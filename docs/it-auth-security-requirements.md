# IT security requirements for SharePoint Graph access

Last updated: 2026-03-11

> [!IMPORTANT]
> This document is the source of truth for production approval decisions related to authentication and data access security.

This document captures DWR Department of Technology Service's requirements for common scientific applications that use Microsoft Graph API and translates them into developer-facing implementation requirements.

## Summary (TL;DR)

- Use app-only auth with a confidential client and certificate in controlled runtime.
- Use `Sites.Selected` with per-site grants, not broad tenant-wide list read scope.
- Implement and evidence controls for sign-in gating, Conditional Access, token/data security, monitoring, and governance.

## Table of contents

- [Audience](#audience)
- [Scope](#scope)
- [Target state](#target-state)
- [Requirements](#requirements)
  - [1. Minimize scope and blast radius](#1-minimize-scope-and-blast-radius)
  - [2. Gate app sign-in (Enterprise App controls)](#2-gate-app-sign-in-enterprise-app-controls)
  - [3. Enforce conditional access](#3-enforce-conditional-access)
  - [4. Secure token handling](#4-secure-token-handling)
  - [5. Data handling controls](#5-data-handling-controls)
  - [6. Monitoring and response](#6-monitoring-and-response)
  - [7. Governance hygiene](#7-governance-hygiene)
- [Evidence checklist](#evidence-checklist)

## Audience

- Developers maintaining this repository and related repositories
- IT/security reviewers
- Team members requesting or approving access

## Scope

Applies to authentication, authorization, runtime, token handling, and operational controls for Microsoft Graph access to SharePoint lists.

## Target state

- Minimize scope and blast radius.
- Prefer app-only access with site-scoped permission (`Sites.Selected`) over broad delegated read access.
- Add policy, monitoring, and governance controls for secure operation.

## Requirements

### 1. Minimize scope and blast radius

#### 1.1 Validate broad permission necessity

**Requirement**
- Confirm whether `Sites.Read.All` is truly required. In almost all cases, it will not be required.
- If not required, remove it.

**Implementation Expectation**
- Document exactly which SharePoint sites/lists are needed and develop accordingly.
- Provide a technical justification if broad tenant-wide read is requested.

#### 1.2 Prefer app-only with `Sites.Selected`

**Requirement**
- Use application permissions with `Sites.Selected`.
- Grant access only to the specific SharePoint sites used by this program.

**Implementation Expectation**
- Register app as confidential client.
- Apply per-site grants rather than tenant-wide read.
- Keep a maintained inventory of approved site IDs/URLs.

#### 1.3 Use certificate auth in controlled runtime

**Requirement**
- Authenticate using certificate-based confidential client auth.
- Run in controlled compute (for example Azure Function or managed VM), not unmanaged public-client endpoints.

**Implementation Expectation**
- Store certificate/private key in approved secret/certificate store.
- Limit local interactive auth usage to development-only scenarios approved by IT.

### 2. Gate app sign-in (Enterprise App controls)

**Requirement**
- Set `User assignment required` on Enterprise App.
- Assign only approved users/groups (prefer dedicated security group).
- Prefer single-tenant app registration unless multi-tenant is explicitly required.

**Implementation Expectation**
- Maintain group ownership and review membership regularly.
- Document assigned groups and business owner.

### 3. Enforce conditional access

**Requirement**
- Require MFA and modern auth.
- Require compliant or hybrid-joined devices when run from endpoints.
- Set sign-in frequency (reauth interval defined by security policy).
- Apply session controls (disable persistent browser sessions; enable token protection if available).

**Implementation Expectation**
- Attach Enterprise App to named conditional access policy set.
- Keep policy references in team runbook.

### 4. Secure token handling

**Requirement**
- Avoid plaintext token caching.
- Store tokens only in protected secure storage, or disable caching if policy requires.
- Do not log tokens, device codes, or other sensitive auth artifacts.
- Rotate/revoke tokens immediately if compromise is suspected.

**Implementation Expectation**
- Review code and logs for sensitive output.
- Add incident playbook steps for token revocation.

### 5. Data handling controls

**Requirement**
- Write outputs only to approved encrypted storage locations.
- Apply DLP and retention policies to output data.
- Maintain auditability for which sites/lists were read and when.

**Implementation Expectation**
- Define approved output path(s) per environment.
- Include run metadata (timestamp, source site/list, actor/app identity) in audit trail.

### 6. Monitoring and response

**Requirement**
- Enable Entra sign-in logs and audit logs; use Defender for Cloud Apps (MCAS) visibility where available.
- Alert on unusual volume, unusual site targets, and unexpected new sign-ins to the app.
- Maintain a break-glass procedure to quickly disable the Enterprise App.

**Implementation Expectation**
- Route alerts to an owned on-call/security channel.
- Test break-glass disable procedure at least once.

### 7. Governance hygiene

**Requirement**
- Use verified internal publisher identity.
- Use clear, non-confusable app naming.
- Store code in reviewed repository with peer review and dependency scanning.
- Document data lineage and business purpose.

**Implementation Expectation**
- Record app owner, data owner, and review cadence.
- Keep architecture and data-flow documentation current.

---

## Evidence checklist

- [ ] Permission matrix and justification (`Sites.Selected` grants listed by site)
- [ ] Enterprise App assignment configuration screenshot/export
- [ ] Conditional Access policy mapping
- [ ] Token handling/logging review notes
- [ ] Data output location and retention/DLP mapping
- [ ] Monitoring rules and alert destinations
- [ ] Break-glass runbook and test evidence
- [ ] Code review and dependency scan evidence
