import path from "path";
import { Function, Runtime, Code } from "@aws-cdk/aws-lambda";
import { Aws, Construct } from "@aws-cdk/core";
import { Rule } from "@aws-cdk/aws-events";
import { LambdaFunction } from "@aws-cdk/aws-events-targets";
import { PolicyStatement } from "@aws-cdk/aws-iam";

export interface TemplateProps { }

export default class Template extends Construct {
  constructor(scope: Construct, id: string, props: TemplateProps) {
    super(scope, id);
    const {  } = props;

    const lambdaFn = new Function(this, "AthenaDDLReplicator", {
      runtime: Runtime.PYTHON_3_8,
      handler: "index.handler",
      code: Code.fromAsset(path.join(__dirname, "..", "..", "src", "lambda", "athenaReplicator")),
    });

    lambdaFn.addToRolePolicy(new PolicyStatement({
      resources: ["*"],
      actions: ["athena:*"],
    }));

    const eventTarget = new LambdaFunction(lambdaFn);

    const eventRule = new Rule(this, "AthenaDDLRule", {
      eventPattern: {
        source: ["aws.athena"],
        detailType: ["Athena Query State Change"],
        region: [Aws.REGION],
        detail: {
          "statementType": ["DDL"],
          "currentState": ["SUCCEEDED"],
        }
      },
      targets: [eventTarget],
    });


  }
}
