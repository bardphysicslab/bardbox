# BardBox Promotion Governance

Standards are maintained in `bardbox` and demonstrated in
`bardbox-project-template`. Production repositories validate improvements in
real deployments; they are not permanent forks of shared infrastructure.

> When a reusable infrastructure or UI improvement is proven in a production BardBox repository, the work is not considered complete until it has been evaluated for promotion into the BardBox standard and project template.

Evaluation does not require promotion when behavior is project-specific,
security-sensitive outside its original scope, or not yet proven. The decision
and reason should still be recorded. Reusable code should be copied from the
mature implementation with only necessary path/configuration adaptation; do not
create independent versions of an established BardBox pattern.
When an operational standard depends on reusable deployment or configuration-
migration tooling, promote the tooling with the standard so the project
template demonstrates the required workflow rather than documenting it alone.
