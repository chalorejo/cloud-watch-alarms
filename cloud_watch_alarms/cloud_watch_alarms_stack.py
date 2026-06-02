from aws_cdk import (
    Stack,
    aws_budgets as budgets,
)
from constructs import Construct

class CloudWatchAlarmsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the cost filters for commonly explored services
        services_to_track = [
            "Amazon Elastic Compute Cloud - Compute",
            "Amazon Relational Database Service",
            "Amazon DynamoDB",
            "Amazon Bedrock",
            "Amazon SageMaker",
            "Amazon Elastic Container Registry",
            "AWS Glue"
        ]

        # Define the Email subscriber property to reuse
        email_subscriber = budgets.CfnBudget.SubscriberProperty(
            address="charissecardineslorejo@gmail.com",
            subscription_type="EMAIL"
        )

        # Define the budget resource
        budgets.CfnBudget(
            self, "FreeTierGuardrailBudget",
            budget=budgets.CfnBudget.BudgetDataProperty(
                budget_type="COST",
                time_unit="MONTHLY",
                budget_limit=budgets.CfnBudget.SpendProperty(
                    amount=0.01,
                    unit="USD"
                ),
                cost_filters={
                    "Service": services_to_track
                }
            ),
            notifications_with_subscribers=[
                # 50% Threshold Alert
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="FORECASTED",
                        threshold=50,
                        threshold_type="PERCENTAGE"
                    ),
                    subscribers=[email_subscriber]
                ),
                # 60% Threshold Alert
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="FORECASTED",
                        threshold=60,
                        threshold_type="PERCENTAGE"
                    ),
                    subscribers=[email_subscriber]
                ),
                # 95% Threshold Alert
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="FORECASTED",
                        threshold=95,
                        threshold_type="PERCENTAGE"
                    ),
                    subscribers=[email_subscriber]
                )
            ]
        )
