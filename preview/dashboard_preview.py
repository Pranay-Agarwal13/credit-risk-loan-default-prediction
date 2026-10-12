"""
Standalone preview verification script.
Tests mock applicant scoring and prints mock SHAP outputs.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from preview.mock_data import get_mock_portfolio_applicants, get_mock_shap_breakdown

def main():
    print("=================================================================")
    print("Credit Risk Prediction System - Mock UI Verification Preview")
    print("UI preview with sample data; not connected to the trained model.")
    print("=================================================================\n")

    applicants = get_mock_portfolio_applicants(5)
    for app in applicants:
        print(f"[{app['id']}] {app['name']}")
        print(f"  • Profile: ${app['income']:,} Income | ${app['credit']:,} Loan (DTI: {app['dti']:.2f}x)")
        print(f"  • Probability: {app['probability'] * 100:.2f}% -> {app['tier']} Risk Tier")
        print(f"  • Recommended Underwriting Action: {app['action']}")
        
        shap_res = get_mock_shap_breakdown(app["probability"], app["dti"], app["ext_score"])
        pos_names = [f"{d['display_name']} (+{d['shap_value']:.2f})" for d in shap_res["top_drivers"]]
        neg_names = [f"{m['display_name']} ({m['shap_value']:.2f})" for m in shap_res["top_mitigators"]]
        print(f"  • Primary Risk Drivers: {', '.join(pos_names) or 'None'}")
        print(f"  • Mitigating Strengths: {', '.join(neg_names) or 'None'}\n")

if __name__ == "__main__":
    main()
