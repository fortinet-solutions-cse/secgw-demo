# Gemini Context: SecGW Hands-On-Lab (HoL)

This file maintains the architectural context and established conventions for the SecGW demo and lab environment.

## Project Overview
A Fortinet Security Gateway (SecGW) hands-on lab environment utilizing FortiManager (FMG) and FortiAnalyzer (FAZ) to manage multiple FortiGate (SEG) instances.

## Core Architecture & Workflows
- **Top-Level Playbook:** `hol.yml` is the primary entry point. It is designed for both step-by-step lab execution (via tags) and full demo deployments.
- **Initialization Role (`0_init`):** 
    - Handles credential fetching via a Python script (`init.py`).
    - Stores dynamic lab data (Serial Numbers, API Tokens) in `vars/runtime_vars.yml`.
    - Generates per-host `host_vars` for FMG and FAZ.
- **Variable Strategy:**
    - **Static Config:** `group_vars/all.yml` (Common lab settings).
    - **Dynamic Data:** `vars/runtime_vars.yml` (Created during runtime, accessed via `runtime_vars` dictionary).
    - **Explicit Loading:** Roles requiring dynamic data must explicitly load `vars/runtime_vars.yml` in their `hol.yml` play.

## Ansible Configuration (`ansible.cfg`)
- **`hash_behaviour = replace`**: Modern standard. Do not use dictionary merging; use the `combine` filter if merging is required.
- **`inject_facts_as_vars = False`**: Prevents namespace collisions. Access facts via `ansible_facts`.
- **Lab Optimizations**: Host key checking is disabled, and SSH pipelining is enabled for student efficiency.

## Key Conventions
- **Idempotency**: Prioritize native `fortinet.fortimanager` modules over `fmgr_generic` where possible.
- **Encapsulation**: Scripts and specific data files should live within their respective roles (e.g., `roles/0_init/scripts/`).
- **Permissions**: The `0_init` role includes a task to ensure `init.py` is executable (`0755`) to handle environments that do not preserve git execution bits.

## Ongoing Maintenance
- When adding new roles that require SEG Serial Numbers, ensure they reference `runtime_vars.seg1_sn` or `runtime_vars.seg2_sn`.
- Always verify changes against the `ansible-playbook hol.yml --tags init` workflow first.
