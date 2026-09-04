# Single-Member Limited Liability Company Operating Agreement
## [ENTITY NAME] LLC — a Wyoming limited liability company

**STATUS: DRAFT FOR COUNSEL REVIEW. NOT LEGAL ADVICE.**

This is a starting document, not an executable instrument. Do not sign it as-is.
It exists so that your US counsel and your German Steuerberater begin from a
concrete text rather than a blank page, and so that the German classification
questions are visible on the face of the document instead of buried.

Prepared 2026-09-04.

---

## READ THIS FIRST — the clauses that decide your German tax outcome

Germany does not accept the US characterisation of your LLC. It runs its own
**Rechtstypenvergleich** under the BMF letter of 19 March 2004, weighing eight
criteria to decide whether the entity is a *Kapitalgesellschaft* (opaque, taxed
as a corporation) or a *Personengesellschaft* (transparent). No single criterion
decides it; the overall picture does.

**That means this document is not administrative boilerplate. It is the primary
evidence in that analysis.** Five clauses below carry most of the weight:

| Clause | Criterion it speaks to | Why it matters |
|---|---|---|
| §4 Management | Centralised management and representation | Manager-managed reads corporate; member-managed reads partnership |
| §7 Transfer | Free transferability of interests | Unrestricted transfer reads corporate |
| §9 Dissolution | Unlimited life / continuity | Perpetual existence reads corporate |
| §6 Distributions | Profit distribution mechanics | Discretionary declared distributions read corporate; automatic allocation reads partnership |
| §5 Capital | Capital contribution requirements | Fixed stated capital reads corporate |

**Do not let anyone — including me — pick these for you before your Steuerberater
has told you which classification you want.** The right answer depends on facts I
do not have: whether §§ 7–14 AStG (Hinzurechnungsbesteuerung) apply, whether your
activity is active under § 8 AStG, and whether the Ort der Geschäftsleitung under
§ 10 AO sits in Germany. Each clause below is marked **[CLASSIFICATION-SENSITIVE]**
with both options stated.

A second warning, unrelated to Germany. If this entity will be the deployer
identity for a token, do not name it "Foundation." Wyoming's naming statute
(W.S. 17-29-108) prohibits a name implying organisation under the Nonprofit
Corporation Act, and separately, a for-profit LLC wearing the word "Foundation"
is a gift to any future adversary arguing the project was presented as
non-commercial. Ask your securities counsel directly before choosing the name.

---

## §1. Formation

1.1 The Company was organised as a Wyoming limited liability company by the
filing of Articles of Organization with the Wyoming Secretary of State on
[DATE], under the Wyoming Limited Liability Company Act, W.S. 17-29-101 et seq.

1.2 The Company's registered agent and registered office in Wyoming are as
stated in the Articles of Organization, as amended from time to time.

1.3 The sole Member is [FULL LEGAL NAME], an individual resident of the Federal
Republic of Germany (the "Member").

1.4 **[CLASSIFICATION-SENSITIVE — capital]** The Member's initial capital
contribution is $[AMOUNT], made on [DATE].

> *Note: a stated fixed capital contribution reads toward corporate
> classification in the Typenvergleich. If transparency is the goal, counsel may
> prefer a nominal or open contribution structure. Separately — and independently
> of German law — record this contribution carefully: for a foreign-owned US
> disregarded entity, the contribution is itself a **reportable transaction**
> under § 6038A, triggering Form 5472. See §11.*

## §2. Name and principal office

2.1 The Company's name is [ENTITY NAME] LLC.

2.2 The Company's principal office is at [ADDRESS].

> **⚠ Do not reflexively enter the registered agent's Wyoming address here.**
> Two separate regimes read this field and they pull in opposite directions:
>
> - **USPTO.** Under Examination Guide 4-19, a juristic entity's domicile is its
>   principal place of business — where senior officers actually direct and
>   control it — not its state of formation. A Wyoming LLC directed from Germany
>   is foreign-domiciled, and US counsel is therefore mandatory under 37 CFR
>   2.11(a). Listing a Wyoming mailbox to escape that requirement is a false
>   domicile statement; the USPTO issues domicile inquiries and a false address
>   can invalidate the application.
> - **German tax.** The same fact — actual management from Germany — is what
>   creates § 10 AO place-of-management exposure.
>
> These are one problem, not two. Answer it once, honestly, with both advisers
> in the room. A Wyoming mailbox does not create management substance and will
> not be treated as if it did.

## §3. Purpose

3.1 The Company is organised for any lawful purpose for which a limited
liability company may be organised under the laws of Wyoming.

3.2 Without limiting §3.1, the Company's anticipated activities include:
holding and licensing intellectual property, including trademarks; developing
and publishing open-source software and open data; and [FURTHER ACTIVITIES — to
be settled with securities counsel before the token architecture is fixed].

> *Note: the stated purpose feeds directly into the § 8 AStG active/passive
> determination. An entity described as holding IP looks passive; an entity
> described as developing and operating software looks more active. Draft this
> clause after your Steuerberater has answered question 7 in the intake list,
> not before. Note also that Wyoming's naming statute prohibits a name implying
> a purpose other than one stated in the Articles — §3 and §2.1 must agree.*

## §4. Management **[CLASSIFICATION-SENSITIVE — centralised management]**

**Option A — Member-managed** *(reads toward partnership / transparency)*

4.1A The Company is managed by its Member. The Member has full authority to
bind the Company and to manage its business and affairs.

**Option B — Manager-managed** *(reads toward corporate / opacity)*

4.1B The Company is managed by one or more Managers appointed by the Member.
The initial Manager is [NAME]. The Managers have exclusive authority to manage
the business and affairs of the Company; the Member in its capacity as such has
no authority to bind the Company.

4.2 [Either option] The Company shall keep records of all material decisions.
Where a decision would be taken in Germany by a person present in Germany, that
fact shall be recorded.

> *§4.2 is deliberately uncomfortable. Contemporaneous records of where decisions
> are actually taken are the evidence base for any § 10 AO position. Creating
> those records only helps you if the position they support is the true one;
> discuss with counsel whether you want this clause at all, because it documents
> the answer either way.*

## §5. Capital contributions

5.1 The Member is not obligated to make additional capital contributions.

5.2 Additional contributions, if made, shall be recorded in the Company's books
with date and amount.

> *Every contribution and every distribution is a reportable transaction for
> Form 5472 purposes. §5.2 and §6.3 exist to make the annual filing mechanical
> rather than reconstructive.*

## §6. Allocations and distributions **[CLASSIFICATION-SENSITIVE — profit distribution]**

**Option A** *(transparency-leaning)* — Profits and losses are allocated to the
Member as they arise. Distributions are made at such times and in such amounts
as the Member determines, subject to W.S. 17-29-405.

**Option B** *(opacity-leaning)* — No Member has any right to a distribution
until a distribution is declared. Profits accumulate in the Company until
declared and distributed.

6.3 All distributions shall be recorded with date, amount and recipient.

## §7. Transfer of interest **[CLASSIFICATION-SENSITIVE — free transferability]**

**Option A** *(transparency-leaning)* — The Member may not transfer all or any
part of its membership interest without [restriction: e.g. unanimous consent of
all members, or a right of first refusal]. A transferee acquires only economic
rights unless admitted as a Member.

**Option B** *(opacity-leaning)* — The Member may freely transfer all or any
part of its membership interest, and a transferee is automatically admitted as
a Member with full rights.

> *This is the single cleanest lever in the Typenvergleich. Free transferability
> is one of the strongest corporate indicators; a meaningful transfer restriction
> is one of the strongest partnership indicators. It is also the clause a token
> project is most likely to want to change later, so decide it deliberately.*

## §8. Liability and indemnification

8.1 The Member is not personally liable for the debts, obligations or
liabilities of the Company solely by reason of being a member, except as
required by the Act.

8.2 The Company shall indemnify the Member and any Manager to the fullest
extent permitted by Wyoming law, except for acts constituting fraud, wilful
misconduct or a knowing violation of law.

> *Ask securities counsel to review §8.2 specifically against the token
> architecture. Indemnification of a deployer for acts taken in that capacity is
> exactly the clause that gets read back in an enforcement posture.*

## §9. Dissolution **[CLASSIFICATION-SENSITIVE — unlimited life]**

**Option A** *(transparency-leaning)* — The Company dissolves upon the death,
incapacity, withdrawal or bankruptcy of the Member, or upon the Member's written
election, unless continuation is elected as provided by the Act.

**Option B** *(opacity-leaning)* — The Company has perpetual existence and does
not dissolve upon any event affecting the Member.

9.2 On dissolution, assets are applied first to creditors, then to the Member.

## §10. Books, records and fiscal year

10.1 The Company maintains books and records at its principal office. The fiscal
year is the calendar year.

10.2 The Company maintains the records required by W.S. 17-29-410 and the
transaction records required by §5.2 and §6.3 of this Agreement.

## §11. Tax matters and mandatory filings

11.1 The Company is a disregarded entity for US federal income tax purposes for
so long as it has a single member and no contrary election is in effect.

11.2 **Form 5472.** The Member acknowledges that a domestic disregarded entity
wholly owned by a foreign person is treated as a corporation for § 6038A
reporting purposes and must file Form 5472 with a pro-forma Form 1120 for any
year in which it has a reportable transaction. Formation, dissolution,
contributions and distributions are all reportable transactions, so a filing
obligation should be assumed from the first year. The return **cannot be
e-filed**. Due 15 April, extendable to 15 October on Form 7004.

> **The penalty is $25,000 for failure to file or for a substantially incomplete
> filing, plus a further $25,000 for each 30-day period the failure continues
> more than 90 days after IRS notice.** There is no small-entity relief and no
> de-minimis exception. This obligation is the single largest recurring risk in
> the structure and it dwarfs every other number in the formation budget.
> Engage a preparer in year one, not in the following April.

11.3 The Company shall maintain a contemporaneous ledger of every reportable
transaction, sufficient to complete Form 5472 without reconstruction.

11.4 The Member acknowledges that German tax treatment is determined
independently of US characterisation, and that classification, place of
management, Hinzurechnungsbesteuerung and any § 138(2) AO notification duty
require separate German advice.

## §12. Amendment; governing law

12.1 This Agreement may be amended only by a writing signed by the Member.

12.2 This Agreement is governed by the laws of the State of Wyoming.

12.3 If any provision is held unenforceable, the remainder continues in effect.

---

**IN WITNESS WHEREOF**, the undersigned has executed this Agreement as of
[DATE].

_______________________________
[FULL LEGAL NAME], Sole Member

---

## Open items before this can be signed

1. **Entity name** — settle the "Foundation" question with securities counsel first.
2. **§4, §6, §7, §9, §1.4** — five classification-sensitive elections, all to be made on the Steuerberater's advice, and all pointing the same direction rather than a mix.
3. **§2.2 principal office** — one honest answer, coordinated between US trademark counsel and the Steuerberater.
4. **§3.2 purpose** — drafted after the § 8 AStG active/passive read, and consistent with the Articles.
5. **§8.2 indemnification** — reviewed against the token architecture.
6. **Whether a Wyoming LLC is the right vehicle at all** — a Wyoming DAO LLC, a DUNA, or a German UG/GmbH may fit better. Ask this before spending on formation, not after.

*This document is a drafting aid. It is not legal or tax advice and creates no
attorney-client relationship. Wyoming counsel should review the Wyoming law
points; a German Steuerberater should decide the classification-sensitive
elections; US securities counsel should review §3.2 and §8.2.*
