"""
=============================================================================
MODUL 04: PELATIHAN 3 MODEL MACHINE LEARNING & EVALUASI ILMIAH BERTINGKAT
Bali Smart Villa & Homestay Pricing Engine (Pure ML 3-Model Benchmark)
=============================================================================
Model yang dilatih & dibandingkan:
1. Random Forest Regressor (Baseline Ensemble Bagging)
2. XGBoost Regressor (Extreme Gradient Boosting)
3. CatBoost Regressor (Champion Model dengan Native Target Statistics)
=============================================================================
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import xgboost as xgb
from catboost import CatBoostRegressor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_CSV = os.path.join(BASE_DIR, "data", "processed", "dataset_train.csv")
TEST_CSV = os.path.join(BASE_DIR, "data", "processed", "dataset_test.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

RF_PARAMS = {
    "n_estimators": 300,
    "max_depth": 14,
    "min_samples_leaf": 2,
    "random_state": 42,
    "n_jobs": -1,
}
XGB_PARAMS = {
    "n_estimators": 350,
    "learning_rate": 0.035,
    "max_depth": 5,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
    "n_jobs": 2,
}
CB_PARAMS = {
    "iterations": 600,
    "learning_rate": 0.035,
    "depth": 6,
    "l2_leaf_reg": 3.0,
    "loss_function": "RMSE",
    "thread_count": 2,
    "random_seed": 42,
    "allow_writing_files": False,
    "verbose": 0,
}


def build_tree_pipeline(regressor, num_cols, cat_cols):
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ]
    )
    return Pipeline([("prep", preprocessor), ("model", regressor)])


def evaluate_metrics(y_true_log, y_pred_log):
    r2 = r2_score(y_true_log, y_pred_log)
    y_true = np.expm1(y_true_log)
    y_pred = np.expm1(y_pred_log)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    med_ae = np.median(np.abs(y_true - y_pred))
    med_ape = np.median(np.abs(y_true - y_pred) / y_true) * 100
    return r2, mae, rmse, med_ae, med_ape


def main():
    print("=" * 75)
    print(" [MODUL 04] PELATIHAN DAN KOMPARASI 3 MODEL MACHINE LEARNING UTAMA")
    print("=" * 75)

    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    train_df = pd.read_csv(TRAIN_CSV)
    test_df = pd.read_csv(TEST_CSV)

    cat_cols = ['regency', 'sub_district', 'property_type']
    for c in cat_cols:
        train_df[c] = train_df[c].fillna('Unknown').astype(str)
        test_df[c] = test_df[c].fillna('Unknown').astype(str)

    non_feature_cols = ['room_id', 'name', 'price_idr', 'log_price']
    num_cols = [c for c in train_df.columns if c not in cat_cols + non_feature_cols]

    print(f"[*] Jumlah Data Latih : {len(train_df)} baris (80%)")
    print(f"[*] Jumlah Data Uji   : {len(test_df)} baris (20%)")
    print(f"[*] Fitur Numerik     : {len(num_cols)} kolom")
    print(f"[*] Fitur Kategori    : {cat_cols}")

    feature_cols = num_cols + cat_cols
    X_train_raw = train_df[feature_cols].copy()
    y_train_log = train_df['log_price'].values
    X_test_raw = test_df[feature_cols].copy()
    y_test_log = test_df['log_price'].values

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    results = []

    oof_rf = np.zeros(len(train_df))
    oof_xgb = np.zeros(len(train_df))
    oof_cb = np.zeros(len(train_df))

    print("\n[1/4] Menjalankan 5-Fold Out-of-Fold Cross Validation (Zero Leakage Pipeline)...")
    for train_idx, val_idx in kf.split(X_train_raw):
        X_tr, X_va = X_train_raw.iloc[train_idx], X_train_raw.iloc[val_idx]
        y_tr = y_train_log[train_idx]

        # 1. Random Forest Fold (Imputer + OneHotEncoder fit strictly on X_tr)
        rf_fold = build_tree_pipeline(RandomForestRegressor(**RF_PARAMS), num_cols, cat_cols)
        rf_fold.fit(X_tr, y_tr)
        oof_rf[val_idx] = rf_fold.predict(X_va)

        # 2. XGBoost Fold (Imputer + OneHotEncoder fit strictly on X_tr)
        xgb_fold = build_tree_pipeline(xgb.XGBRegressor(**XGB_PARAMS), num_cols, cat_cols)
        xgb_fold.fit(X_tr, y_tr)
        oof_xgb[val_idx] = xgb_fold.predict(X_va)

        # 3. CatBoost Fold (Native ordered target statistics & NaN handling)
        cb_fold = CatBoostRegressor(cat_features=cat_cols, **CB_PARAMS)
        cb_fold.fit(X_tr, y_tr)
        oof_cb[val_idx] = cb_fold.predict(X_va)

    rf_oof_r2, rf_oof_mae, _, _, _ = evaluate_metrics(y_train_log, oof_rf)
    xgb_oof_r2, xgb_oof_mae, _, _, _ = evaluate_metrics(y_train_log, oof_xgb)
    cb_oof_r2, cb_oof_mae, _, _, _ = evaluate_metrics(y_train_log, oof_cb)

    # -------------------------------------------------------------
    # PELATIHAN MODEL LENGKAP PADA DATA LATIH & EVALUASI DATA UJI
    # -------------------------------------------------------------
    print("\n[2/4] Melatih Model 1: Random Forest Regressor (Baseline)...")
    rf_model = build_tree_pipeline(RandomForestRegressor(**RF_PARAMS), num_cols, cat_cols)
    rf_model.fit(X_train_raw, y_train_log)
    rf_test_pred = rf_model.predict(X_test_raw)
    rf_r2, rf_mae, rf_rmse, rf_medae, rf_medape = evaluate_metrics(y_test_log, rf_test_pred)
    results.append({
        "Model": "Random Forest (Baseline)",
        "CV_R2_Mean": rf_oof_r2,
        "CV_MAE_IDR": rf_oof_mae,
        "Test_R2": rf_r2,
        "Test_MAE_IDR": rf_mae,
        "Test_MedAE_IDR": rf_medae,
        "Test_RMSE_IDR": rf_rmse,
        "Test_MdAPE_Pct": rf_medape
    })
    print(f" -> RF Test R2: {rf_r2:.4f} | CV R2: {rf_oof_r2:.4f} | MAE: Rp {rf_mae:,.0f} | MedAE: Rp {rf_medae:,.0f}")

    print("\n[3/4] Melatih Model 2: XGBoost Regressor...")
    xgb_model = build_tree_pipeline(xgb.XGBRegressor(**XGB_PARAMS), num_cols, cat_cols)
    xgb_model.fit(X_train_raw, y_train_log)
    xgb_test_pred = xgb_model.predict(X_test_raw)
    xgb_r2, xgb_mae, xgb_rmse, xgb_medae, xgb_medape = evaluate_metrics(y_test_log, xgb_test_pred)
    results.append({
        "Model": "XGBoost Regressor",
        "CV_R2_Mean": xgb_oof_r2,
        "CV_MAE_IDR": xgb_oof_mae,
        "Test_R2": xgb_r2,
        "Test_MAE_IDR": xgb_mae,
        "Test_MedAE_IDR": xgb_medae,
        "Test_RMSE_IDR": xgb_rmse,
        "Test_MdAPE_Pct": xgb_medape
    })
    print(f" -> XGBoost Test R2: {xgb_r2:.4f} | CV R2: {xgb_oof_r2:.4f} | MAE: Rp {xgb_mae:,.0f} | MedAE: Rp {xgb_medae:,.0f}")

    print("\n[4/4] Melatih Model 3: CatBoost Regressor...")
    cb_model = CatBoostRegressor(cat_features=cat_cols, **CB_PARAMS)
    cb_model.fit(X_train_raw, y_train_log)
    cb_test_pred = cb_model.predict(X_test_raw)
    cb_r2, cb_mae, cb_rmse, cb_medae, cb_medape = evaluate_metrics(y_test_log, cb_test_pred)

    cb_model.save_model(os.path.join(MODELS_DIR, "catboost_pricing_model.cbm"))
    results.append({
        "Model": "CatBoost Regressor",
        "CV_R2_Mean": cb_oof_r2,
        "CV_MAE_IDR": cb_oof_mae,
        "Test_R2": cb_r2,
        "Test_MAE_IDR": cb_mae,
        "Test_MedAE_IDR": cb_medae,
        "Test_RMSE_IDR": cb_rmse,
        "Test_MdAPE_Pct": cb_medape
    })
    print(f" -> CatBoost Test R2: {cb_r2:.4f} | CV R2: {cb_oof_r2:.4f} | MAE: Rp {cb_mae:,.0f} | MedAE: Rp {cb_medae:,.0f} | MdAPE: {cb_medape:.2f}%")

    # Hapus artefak model pembanding yang tidak dipakai pada inferensi agar repositori tetap ringkas
    for stale_model in ["random_forest_model.joblib", "xgboost_model.joblib"]:
        stale_path = os.path.join(MODELS_DIR, stale_model)
        if os.path.exists(stale_path):
            os.remove(stale_path)

    feature_cols_encoded = list(rf_model.named_steps["prep"].get_feature_names_out())
    joblib.dump({
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "all_features": feature_cols,
        "feature_cols_encoded": feature_cols_encoded
    }, os.path.join(MODELS_DIR, "feature_metadata.joblib"))

    # -------------------------------------------------------------
    # REKAPITULASI KOMPARASI 3 MODEL & EVALUASI PER KELAS HARGA
    # -------------------------------------------------------------
    bench_df = pd.DataFrame(results)
    bench_df = bench_df.sort_values(by="Test_R2", ascending=False).reset_index(drop=True)
    bench_df.to_csv(os.path.join(REPORTS_DIR, "model_benchmark_results.csv"), index=False)

    actual_idr = np.expm1(y_test_log)
    pred_idr = np.expm1(cb_test_pred)

    tier_defs = [
        ("Homestay / Budget (< Rp 750 Ribu)", 0, 750000, "Kamar Pribadi & Homestay"),
        ("Villa Reguler (Rp 750 Ribu - Rp 2,5 Juta)", 750000, 2500000, "Villa 1-2 Kamar Populer"),
        ("Villa Menengah (Rp 2,5 Juta - Rp 6 Juta)", 2500000, 6000000, "Villa 2-4 Kamar Kolam Renang"),
        ("Villa Premium (Rp 6 Juta - Rp 10 Juta)", 6000000, 10500000, "Villa Mewah 3-6 Kamar")
    ]
    tier_rows = []
    for t_name, low_val, high_val, t_desc in tier_defs:
        mask = (actual_idr >= low_val) & (actual_idr < high_val)
        cnt = int(mask.sum())
        if cnt > 0:
            t_actual_mean = float(np.mean(actual_idr[mask]))
            t_pred_mean = float(np.mean(pred_idr[mask]))
            t_mae = float(mean_absolute_error(actual_idr[mask], pred_idr[mask]))
            t_medae = float(np.median(np.abs(actual_idr[mask] - pred_idr[mask])))
            t_mdape = float(np.median(np.abs(actual_idr[mask] - pred_idr[mask]) / actual_idr[mask]) * 100)
            tier_rows.append({
                "Kelas_Penginapan": t_name,
                "Jumlah_Sampel_Uji": cnt,
                "Rata_Rata_Aktual_IDR": t_actual_mean,
                "Rata_Rata_Prediksi_IDR": t_pred_mean,
                "MAE_IDR": t_mae,
                "MedAE_IDR": t_medae,
                "MdAPE_Pct": t_mdape,
                "Karakteristik_Properti": t_desc
            })

    tier_df = pd.DataFrame(tier_rows)
    tier_df.to_csv(os.path.join(REPORTS_DIR, "tier_accuracy_breakdown.csv"), index=False)

    print("\n" + "=" * 75)
    print(" [TABEL KOMPARASI AKURASI 3 MODEL MACHINE LEARNING UTAMA]")
    print("=" * 75)
    print(bench_df.to_string(index=False))
    print("\n" + "=" * 75)
    print(" [RINCIAN AKURASI PER KELAS PASAR PENGINAPAN (CATBOOST)]")
    print("=" * 75)
    print(tier_df.to_string(index=False))
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
