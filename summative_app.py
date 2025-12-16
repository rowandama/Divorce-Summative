# Divorce Probability Dashboard
# (Agency vs Structure)
# This Shiny app estimates divorce probabilities based on user-inputted
 
from shiny import App, ui, render, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
 
 
 
# Load dataset
divorce = pd.read_csv('/Users/macbookair/Downloads/data/Divorce-Summative/divorce_df.csv')

 
 
# Fit logistic regression models
 
 
# Internal relationship factors (agency)
model_internal = smf.logit(
    "divorced ~ communication_score + infidelity_occurred + domestic_violence_history",
    data=divorce
).fit(disp=False)
 
# Structural factors
model_structural = smf.logit(
    "divorced ~ mental_health_issues + C(education_level) + social_support",
    data=divorce
).fit(disp=False)
 
# Combined model
model_combined = smf.logit(
    "divorced ~ communication_score + infidelity_occurred + domestic_violence_history + mental_health_issues + social_support",
    data=divorce
).fit(disp=False)
 
 
# User Interface
 
 
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Relationship Profile"),
 
        ui.input_slider(
            "communication",
            "Communication Quality",
            min=1, max=10, value=5
        ),
 
        ui.input_select(
            "infidelity",
            "Infidelity Occurred",
            choices={"0": "No", "1": "Yes"}
        ),
 
        ui.input_select(
            "violence",
            "Domestic Violence History",
            choices={"0": "No", "1": "Yes"}
        ),
 
        ui.input_select(
            "mental_health",
            "Mental Health Issues",
            choices={"0": "No", "1": "Yes"}
        ),
 
        ui.input_slider(
            "social_support",
            "Social Support Level",
            min=1, max=10, value=5
        ),
 
        ui.input_select(
            "education",
            "Highest Education Level",
            choices=["High School", "Undergraduate", "Masters", "PhD"]
        ),
    ),
 
    ui.layout_columns(
        ui.card(
            ui.h4("Internal Factors Model"),
            ui.output_text("pred_internal")
        ),
        ui.card(
            ui.h4("Structural Factors Model"),
            ui.output_text("pred_structural")
        ),
        ui.card(
            ui.h4("Combined Model"),
            ui.output_text("pred_combined")
        ),
        col_widths=[4, 4, 4]
    ),
 
    ui.hr(),
 
    ui.h3("Predicted Divorce Probability by Model"),
    ui.output_plot("probability_barplot"),
 
    ui.hr(),
 
    ui.h3("Effect of Communication Quality (Holding Others Constant)"),
    ui.output_plot("communication_effect"),
 
    ui.hr(),
    ui.p(
        "Predictions are based on a simulated dataset and are intended "
        "for educational and analytical purposes only."
    ),
 
    title="Agency vs Structure: Divorce Risk Dashboard"
)
 
 
# Server
 
 
def server(input, output, session):
 
 
    # Shared reactive calculation
  
    @reactive.Calc
    def predicted_probabilities():
        """
        Compute predicted divorce probabilities for all three models.
        Recalculates automatically when any input changes.
        """
 
        internal_df = pd.DataFrame({
            "communication_score": [input.communication()],
            "infidelity_occurred": [int(input.infidelity())],
            "domestic_violence_history": [int(input.violence())],
        })
 
        structural_df = pd.DataFrame({
            "mental_health_issues": [int(input.mental_health())],
            "education_level_PhD": [1 if input.education() == "PhD" else 0],
            "social_support": [input.social_support()],
        })
 
        combined_df = pd.DataFrame({
            "communication_score": [input.communication()],
            "infidelity_occurred": [int(input.infidelity())],
            "domestic_violence_history": [int(input.violence())],
            "mental_health_issues": [int(input.mental_health())],
            "social_support": [input.social_support()],
        })
 
        return {
            "internal": model_internal.predict(internal_df)[0],
            "structural": model_structural.predict(structural_df)[0],
            "combined": model_combined.predict(combined_df)[0],
        }
 
 
    # Text outputs (explicit @output)
  
 
    @output
    @render.text
    def pred_internal():
        prob = predicted_probabilities()["internal"]
        return f"Estimated probability of divorce: {prob:.1%}"
 
    @output
    @render.text
    def pred_structural():
        prob = predicted_probabilities()["structural"]
        return f"Estimated probability of divorce: {prob:.1%}"
 
    @output
    @render.text
    def pred_combined():
        prob = predicted_probabilities()["combined"]
        return f"Estimated probability of divorce: {prob:.1%}"
 
 
    # Bar plot comparing models
 
 
    @output
    @render.plot
    def probability_barplot():
        probs = predicted_probabilities()
 
        labels = ["Internal", "Structural", "Combined"]
        values = [probs["internal"], probs["structural"], probs["combined"]]
 
        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Predicted Probability of Divorce")
        ax.set_title("Comparison of Model Predictions")
 
        fig.tight_layout()
        return fig
 
    #
    # Marginal effect plot (agency)
    # The marginal effect plot isolates the effect of communication quality on divorce risk. (Helps analyse the agency question)
 
    @output
    @render.plot
    def communication_effect():
        comm_range = np.arange(1, 11)
 
        df = pd.DataFrame({
            "communication_score": comm_range,
            "infidelity_occurred": int(input.infidelity()),
            "domestic_violence_history": int(input.violence()),
            "mental_health_issues": int(input.mental_health()),
            "social_support": input.social_support(),
        })
 
        probs = model_combined.predict(df)
 
        fig, ax = plt.subplots()
        ax.plot(comm_range, probs)
        ax.set_ylim(0, 1)
        ax.set_xlabel("Communication Quality")
        ax.set_ylabel("Predicted Probability of Divorce")
        ax.set_title("Effect of Communication Quality")
 
        fig.tight_layout()
        return fig
 
 
 
# Run the app
 
 
app = App(app_ui, server)