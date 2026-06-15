# CRM Schema — Twenty

Object definitions for the CRM layer, powered by [Twenty](https://twenty.com) (self-hosted, `localhost:3001`).

> **Legend:** `sys` = system-generated, read-only · `app` = Twenty built-in · `cus` = custom field
>
> **Last verified:** 2026-06-14 via GraphQL introspection

Replace `{{CRM_URL}}` with your Twenty instance URL (default: `http://localhost:3001`).

---

## GraphQL Endpoints

| Endpoint | Purpose |
|---|---|
| `POST {{CRM_URL}}/graphql` | Data CRUD |
| `POST {{CRM_URL}}/metadata` | Schema introspection |

Auth: `Authorization: Bearer {{TWENTY_API_KEY}}`

---

## COMPANY

### App fields

| Field | Type |
|---|---|
| `name` | TEXT |
| `domainName` | LINKS |
| `address` | ADDRESS |
| `annualRevenue` | CURRENCY |
| `linkedinLink` | LINKS |
| `accountOwner` | RELATION M:1 → WorkspaceMember |
| `people` | RELATION 1:M → Person |
| `opportunities` | RELATION 1:M → Opportunity |
| `noteTargets` | RELATION 1:M |
| `taskTargets` | RELATION 1:M |

### Custom fields

| Field | Type | Options |
|---|---|---|
| `accountType` | SELECT | `PROSPECT` `LEAD` `CLIENT` `PARTNER` `OPT_OUT` |
| `country` | SELECT | `TAIWAN` `MALAYSIA` `INDONESIA` `THAILAND` `SINGAPORE` `VIETNAM` `OTHER` |
| `industry` | MULTI_SELECT | `GOVERNMENT` `WATER_UTILITIES` |
| `companyOverview` | TEXT | |
| `enrichmentOverview` | TEXT | |
| `registeredNameEn` | TEXT | |
| `registeredNameCh` | TEXT | |
| `companyEmail` | EMAILS | |
| `companyPhone` | PHONES | |
| `lastContactDate` | DATE_TIME | |
| `lastEnrichedDate` | DATE_TIME | |
| `partnerships` | RELATION 1:M | |
| `engagements` | RELATION 1:M | |

---

## PERSON

### App fields

| Field | Type |
|---|---|
| `name` | FULL_NAME |
| `emails` | EMAILS |
| `phones` | PHONES |
| `jobTitle` | TEXT |
| `linkedinLink` | LINKS |
| `company` | RELATION M:1 → Company |

### Custom fields

| Field | Type | Options |
|---|---|---|
| `status` | SELECT | `PROSPECT` `LEAD` `CLIENT` `PARTNER` `OPT_OUT` |
| `country` | SELECT | `TAIWAN` `HONG_KONG` `CHINA` `MALAYSIA` `THAILAND` `INDONESIA` `JAPAN` |
| `preferredChannel` | SELECT | `EMAIL` `WHATSAPP` `LINE` `PHONE` |
| `decisionRole` | SELECT | `BUYER` `USER` `INFLUENCER` `BLOCKER` `CHAMPION` |
| `source` | SELECT | `REFERRAL` `EVENT` `PARTNER` `NETWORK` `INBOUND_WEB` `OUTBOUND_MAYA` |
| `department` | TEXT | |
| `remarks` | TEXT | |
| `lastContactDate` | DATE_TIME | |
| `relatedPartnerships` | RELATION M:1 → Partnership | |
| `primaryPartnerships` | RELATION 1:M → Partnership | |
| `engagementsAttended` | RELATION M:1 → Engagement | |
| `involvingOpportunities` | RELATION M:1 → Opportunity | |

---

## OPPORTUNITY

### App fields

| Field | Type | Options |
|---|---|---|
| `name` | TEXT | |
| `amount` | CURRENCY | |
| `closeDate` | DATE_TIME | |
| `stage` | SELECT | `NEW` `SCREENING` `MEETING` `PROPOSAL` `CUSTOMER` |
| `company` | RELATION M:1 | |
| `owner` | RELATION M:1 → WorkspaceMember | |
| `pointOfContact` | RELATION M:1 → Person | |

### Custom fields

| Field | Type | Options |
|---|---|---|
| `businessLine` | SELECT | `BUSYCOW` `GEOKERNEL` `AQUAOPTIMA` `TRACI` `DISTIFY` `DATAXQUAD` |
| `dealType` | SELECT | `DIRECT` `PARTNERLED` |
| `healthCheck` | SELECT | `ON_TRACK` `NEEDS_FOLLOWUP` `AWAITING_RESPONSE` `AT_RISK` |
| `priority` | SELECT | `HIGH` `MEDIUM` `LOW` |
| `probability` | NUMBER | |
| `overview` | TEXT | |
| `currentStatusSummary` | TEXT | |
| `nextActionSummary` | TEXT | |
| `nextFollowUpDate` | DATE_TIME | |
| `lastUpdateDate` | DATE_TIME | |
| `primaryContact` | TEXT | text annotation |
| `otherContacts` | RELATION 1:M → Person | |
| `engagements` | RELATION 1:M → Engagement | |

---

## PARTNERSHIP

### App fields

| Field | Type |
|---|---|
| `name` | TEXT |

### Custom fields

| Field | Type | Options |
|---|---|---|
| `stage` | SELECT | `PROSPECT` `QUALIFYING` `AGREEMENT` `ACTIVE` `INACTIVE` |
| `status` | SELECT | `ACTIVE` `NEEDS_FOLLOWUP` `DORMANT` `INACTIVE` |
| `partnerType` | SELECT | `RESELLER` `INTEGRATOR` `TECHNOLOGY` `REFERRAL` |
| `partnershipOverview` | TEXT | |
| `currentStatusSummary` | TEXT | |
| `nextActionSummary` | TEXT | |
| `startDate` | DATE_TIME | |
| `endDate` | DATE_TIME | |
| `lastUpdateDate` | DATE_TIME | |
| `docLink` | LINKS | |
| `company` | RELATION M:1 → Company | |
| `owner` | RELATION M:1 → WorkspaceMember | |
| `primaryContact` | RELATION M:1 → Person | |
| `relatedPeople` | RELATION 1:M → Person | |
| `engagements` | RELATION 1:M → Engagement | |
| `tasks` | RELATION 1:M → Task | |

---

## ENGAGEMENT

### Custom fields

| Field | Type | Options |
|---|---|---|
| `engagementType` | SELECT | `PHONE` `INPERSON` `ONLINE` `MESSAGING` `DEMO` `EMAIL` `EVENT` |
| `engagementStatus` | SELECT | `PLANNED` `COMPLETED` |
| `channel` | SELECT | `EMAIL` `WHATSAPP` `LINE` `PHONE` `IN_PERSON` `ZOOM` `TEAMS` |
| `engagementDate` | DATE_TIME | |
| `engagementNote` | RICH_TEXT | |
| `nextAction` | TEXT | |
| `outcome` | TEXT | |
| `company` | RELATION M:1 → Company | |
| `opportunity` | RELATION M:1 → Opportunity (optional) | |
| `partnership` | RELATION M:1 → Partnership (optional) | |
| `clientAttendees` | RELATION 1:M → Person | |
| `ourTeam` | RELATION 1:M → WorkspaceMember | |

---

## TASK

### App fields

| Field | Type | Options |
|---|---|---|
| `title` | TEXT | |
| `status` | SELECT | `TODO` `IN_PROGRESS` `DONE` |
| `dueAt` | DATE_TIME | |
| `bodyV2` | RICH_TEXT | |
| `assignee` | RELATION M:1 → WorkspaceMember | |

### Custom fields

| Field | Type | Options |
|---|---|---|
| `taskPriority` | SELECT | `HIGH` `MEDIUM` `LOW` |
| `agentAdvice` | RICH_TEXT | |
| `taskResults` | RICH_TEXT | |
| `partnership` | RELATION M:1 → Partnership (optional) | |
| `opportunity` | RELATION M:1 → Opportunity (optional) | |

---

## Relationship Map

```
Company ──┬── People          (1:M)
          ├── Opportunities   (1:M)
          ├── Partnerships    (1:M)
          └── Engagements     (1:M)

Opportunity ──┬── Engagements     (1:M)
              └── Other Contacts  (1:M → Person)

Partnership ──┬── Engagements     (1:M)
              ├── Tasks           (1:M)
              ├── Primary Contact (M:1 → Person)
              └── Related People  (1:M → Person)

Engagement ──┬── Company          (M:1)
             ├── Opportunity      (M:1, optional)
             ├── Partnership      (M:1, optional)
             ├── Client Attendees (1:M → Person)
             └── Our Team         (1:M → WorkspaceMember)

Task ──┬── Opportunity  (M:1, optional)
       └── Partnership  (M:1, optional)
```

---

## Changelog

| Date | Change |
|---|---|
| 2026-06-14 | Corrected Opportunity stages (`NEW/SCREENING/MEETING/PROPOSAL/CUSTOMER`); fixed `healthCheck` (`AWAITING_RESPONSE` not `AWAITING`); fixed `dealType` (`PARTNERLED` not `PARTNERSHIP/INVESTMENT`); added `businessLine` field; removed `VERY_HIGH` from priority |
| 2026-06-12 | Unified `accountType` SELECT replacing `accountStatus` + `accountType` MULTI_SELECT |
| 2026-06-11 | Initial schema |
