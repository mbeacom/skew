import os
from typing import Any, Dict, List, Optional

import skew
from skew.arn import ARN

IGNORED_GLOBAL_SERVICES: List[str] = os.environ.get("IGNORED_GLOBAL_SERVICES", "route53,iam").split(",")


def get_services():
    arn_obj: ARN = ARN()
    services = arn_obj.service.choices()
    services.sort()
    print(type(services))
    return services


def get_inventory(services: Optional[Any] = None) -> Dict[str, Any]:
    """Get the AWS inventory."""
    inventory: Dict[str, Any] = {}

    if not services:
        services = get_services()

    print("Enumerating all resources in the following services: " + " ".join(services) + "\n")

    for service in services:
        inventory[service] = {}
        if service in IGNORED_GLOBAL_SERVICES:
            print(service)
            print("Skipping global services")
            uri: str = f"arn:aws:{service}::*:*/*"
            try:
                arn = skew.scan(uri)
                inventory[service]["arn"] = arn
                inventory[service]["arns"] = []
                for i in arn:
                    inventory[service]["arns"].append(i.arn)
                    print(i.arn)
            except Exception as e:
                print(f"Exception encountered while attempting to scan the global service: ({service}) - Error: ({e})")
        else:
            print(f"Service: ({service.upper()})")
            uri = f"arn:aws:{service}:*:*:*/*"
            try:
                arn = skew.scan(uri)
                inventory[service]["arn"] = arn
                inventory[service]["arns"] = []
                for i in arn:
                    inventory[service]["arns"].append(i.arn)
                    print(i.arn)
            except Exception as e:
                print(
                    f"Exception encountered while attempting to scan the standard service: ({service}) - Error: ({e})"
                )
    return inventory
