# Requirements Document

## Introduction

The AI Agentic Waste Management Web App is a role-based platform built with Next.js 14 (App Router), BetterAuth, Prisma ORM, Neon (PostgreSQL), Tailwind CSS, and Shadcn UI. The system enables three distinct user roles — Reporter, Collector, and Admin — to participate in a coordinated waste reporting, collection, and verification workflow. Reporters submit waste reports with location and classification data, Collectors claim and fulfill those reports, and Admins oversee user approvals and report verification. A points-based incentive system rewards participation. The landing page features a Waste Classification Gallery, and the UI uses an emerald brand color with Shadcn UI components throughout.

---

## Glossary

- **System**: The AI Agentic Waste Management Web App
- **Reporter**: An authenticated user with the REPORTER role who submits waste reports
- **Collector**: An authenticated user with the COLLECTOR role who collects reported waste
- **Admin**: An authenticated user with the ADMIN role who manages users and verifies collections
- **WasteReport**: A record submitted by a Reporter describing waste at a specific location
- **Feedback**: A text note submitted by a Collector when marking a report as collected
- **BetterAuth**: The authentication library used for session management and user registration
- **Prisma**: The ORM used to interact with the Neon PostgreSQL database
- **Neon**: The serverless PostgreSQL database provider
- **Shadcn_UI**: The component library used for all UI elements
- **Points**: A numeric score awarded to users for participation in the waste management workflow
- **Status_PENDING**: A state indicating an entity is awaiting action (user approval or waste collection)
- **Status_APPROVED**: A state indicating a Collector account has been approved by an Admin
- **Status_COLLECTED**: A state indicating a WasteReport has been marked collected by a Collector
- **Status_VERIFIED**: A state indicating a WasteReport has been verified by an Admin
- **Sidebar**: The global navigation component visible to all authenticated users
- **Dashboard**: The role-specific main interface for authenticated users

---

## Requirements

### Requirement 1: Database Schema

**User Story:** As a developer, I want a well-defined database schema, so that all user, report, and feedback data is stored consistently and relationally.

#### Acceptance Criteria

1. THE System SHALL define a User model with fields: id (unique identifier), email (unique, max 255 characters), name (non-empty, max 100 characters), role (enum: REPORTER, COLLECTOR, ADMIN), status (enum: PENDING, APPROVED), and points (integer, default 0, minimum 0, maximum 999999).
2. THE System SHALL define a WasteReport model with fields: id (unique identifier), location (non-empty String, max 500 characters), wasteType (enum: ORGANIC, PLASTIC, METAL, E_WASTE, HAZARDOUS), amount (non-empty String, max 100 characters), status (enum: PENDING, COLLECTED, VERIFIED), reporterId (foreign key to User, non-nullable), collectorId (foreign key to User, nullable), and createdAt (DateTime, auto-set on creation).
3. THE System SHALL define a Feedback model with fields: id (unique identifier), reportId (foreign key to WasteReport, non-nullable), content (non-empty String, max 500 characters), and createdAt (DateTime, auto-set on creation).
4. THE System SHALL enforce referential integrity such that: deleting a User with existing WasteReports as reporter is prevented or cascades to delete those reports; a WasteReport's reporterId must reference an existing User; a WasteReport's collectorId, when set, must reference an existing User.
5. THE System SHALL enforce a unique constraint on the User model's email field so that no two User records share the same email address.
6. THE Prisma Schema SHALL be the single source of truth for all database models and migrations, and all schema changes SHALL be applied via Prisma migrations.

---

### Requirement 2: User Registration and Authentication

**User Story:** As a visitor, I want to register an account with a chosen role, so that I can access the features appropriate to my role.

#### Acceptance Criteria

1. WHEN a visitor submits a registration form, THE System SHALL create a new User record with the provided email, name, password (hashed), and selected role (one of REPORTER, COLLECTOR, ADMIN).
2. WHEN a visitor submits a registration form, THE System SHALL validate that: the email is a valid email format, the name is non-empty, the role is one of the allowed enum values, and the password is at least 8 characters long; IF any validation fails, THE System SHALL display an error message indicating the cause of failure without creating a User record.
3. WHEN a new User is created with role COLLECTOR, THE System SHALL set the User's status to PENDING.
4. WHEN a new User is created with role REPORTER or ADMIN, THE System SHALL set the User's status to APPROVED.
5. WHEN a visitor submits valid login credentials, THE System SHALL use BetterAuth to create a new session for the User.
6. WHEN an authenticated User logs out, THE System SHALL use BetterAuth to invalidate the current session.
7. THE System SHALL include the authenticated User's role and status in the session payload so that middleware and server actions can read them without an additional database query.
8. IF a visitor submits a registration form with an email that already exists, THEN THE System SHALL return an error message indicating the cause of failure without creating a duplicate User record.
9. IF a visitor submits a login form with invalid credentials, THEN THE System SHALL return an error message indicating the cause of failure without creating a session.

---

### Requirement 3: Middleware and Route Access Control

**User Story:** As a system operator, I want route-level access control enforced by middleware, so that users can only access pages appropriate to their role and status.

#### Acceptance Criteria

1. WHEN an authenticated User with role REPORTER accesses a route under `/dashboard/reporter/`, THE System SHALL allow access.
2. WHEN an authenticated User without role REPORTER attempts to access a route under `/dashboard/reporter/`, THE System SHALL redirect the User to `/dashboard/collector/` if their role is COLLECTOR, or to `/admin/` if their role is ADMIN.
3. WHEN an authenticated User with role COLLECTOR and status APPROVED accesses a route under `/dashboard/collector/`, THE System SHALL allow access.
4. WHEN an authenticated User with role COLLECTOR and status PENDING accesses a route under `/dashboard/collector/`, THE System SHALL redirect the User to the `/pending-approval` page.
5. WHEN an authenticated User with role ADMIN accesses a route under `/admin/`, THE System SHALL allow access.
6. WHEN an authenticated User without role ADMIN attempts to access a route under `/admin/`, THE System SHALL redirect the User to `/dashboard/reporter/` if their role is REPORTER, or to `/dashboard/collector/` if their role is COLLECTOR.
7. WHEN an unauthenticated visitor attempts to access any route under `/dashboard/` or `/admin/`, THE System SHALL redirect the visitor to the `/login` page.
8. WHEN an authenticated User with role COLLECTOR and status PENDING attempts to access any protected route other than `/pending-approval`, THE System SHALL redirect the User to `/pending-approval`.

---

### Requirement 4: Landing Page and Waste Classification Gallery

**User Story:** As a visitor, I want to see an informative landing page with a waste classification gallery, so that I understand the types of waste the platform handles and their environmental impact.

#### Acceptance Criteria

1. THE System SHALL render a publicly accessible landing page at the root route `/` that does not require authentication.
2. THE Landing_Page SHALL display a Waste Classification Gallery containing exactly one card for each waste type: ORGANIC, PLASTIC, METAL, E_WASTE, and HAZARDOUS.
3. THE Landing_Page SHALL display, for each waste type card, the waste type name and a non-empty description of at least 20 characters explaining its impact on nature.
4. THE Landing_Page SHALL display navigation links to the `/login` and `/register` pages.
5. THE Landing_Page SHALL apply the emerald brand color to headings, buttons, and interactive accents, and shall apply white and Tailwind gray-scale shades to backgrounds and body text.
6. THE Landing_Page SHALL use Shadcn_UI Card components for waste type cards, Shadcn_UI Button components for navigation links, and Shadcn_UI navigation components for the header.
7. IF the Landing_Page fails to load, THEN THE System SHALL display a user-facing error message without exposing internal error details.

---

### Requirement 5: Global Sidebar Navigation

**User Story:** As an authenticated user, I want a role-specific sidebar, so that I can navigate to the features available to my role.

#### Acceptance Criteria

1. WHILE a User is authenticated and on any route under `/dashboard/` or `/admin/`, THE Sidebar SHALL be visible and fixed to the left side of the viewport.
2. IF the authenticated User has role REPORTER, THEN THE Sidebar SHALL display navigation links to: Report Waste (`/dashboard/reporter/report`), Leaderboard (`/dashboard/reporter/leaderboard`), and Profile (`/dashboard/reporter/profile`).
3. IF the authenticated User has role COLLECTOR, THEN THE Sidebar SHALL display navigation links to: Collect Waste (`/dashboard/collector/collect`), Leaderboard (`/dashboard/collector/leaderboard`), and Profile (`/dashboard/collector/profile`).
4. IF the authenticated User has role ADMIN, THEN THE Sidebar SHALL display navigation links to: Manage Users (`/admin/users`) and Verify Reports (`/admin/verify`).
5. THE Sidebar SHALL display the authenticated User's name and role label.
6. WHEN the authenticated User activates the logout action in the Sidebar, THE System SHALL terminate the User's session and redirect the User to the `/login` page.
7. THE Sidebar SHALL apply a visually distinct style (e.g., active color or bold weight) to the navigation link corresponding to the currently active route.
8. THE Sidebar SHALL use Shadcn_UI components and apply the emerald brand color as the primary color for active states and interactive elements.

---

### Requirement 6: Reporter Dashboard — Submit and View Reports

**User Story:** As a Reporter, I want to submit waste reports and view my past submissions, so that I can contribute to waste management and track my activity.

#### Acceptance Criteria

1. THE Reporter_Dashboard SHALL display a form for submitting a new WasteReport with fields: location (text input), wasteType (select from enum values: ORGANIC, PLASTIC, METAL, E_WASTE, HAZARDOUS), and amount (text input).
2. WHEN a Reporter submits a waste report form where all required fields are present and wasteType is a valid enum value, THE System SHALL atomically invoke the `submitReport` server action to create a new WasteReport record with status PENDING and the Reporter's id as reporterId, and increment the Reporter's points by 10 in the same transaction.
3. WHEN a Reporter submits a waste report form with one or more missing required fields or an invalid wasteType value, THE System SHALL display a validation error for each invalid field without creating a WasteReport record.
4. THE Reporter_Dashboard SHALL display a list of all WasteReports submitted by the authenticated Reporter, ordered by createdAt descending, showing location, wasteType, amount, status, and createdAt for each.
5. WHEN the Reporter's report list is empty, THE Reporter_Dashboard SHALL display an empty state message.
6. IF the `submitReport` server action fails due to a server or database error, THEN THE System SHALL display an error message to the Reporter without creating a partial WasteReport record or modifying the Reporter's points.

---

### Requirement 7: Collector Dashboard — Collect Waste and Submit Feedback

**User Story:** As an approved Collector, I want to see pending waste reports and mark them as collected with feedback, so that I can fulfill collection tasks and communicate outcomes.

#### Acceptance Criteria

1. THE Collector_Dashboard SHALL display a feed of all WasteReports with status PENDING as individual cards.
2. WHEN a WasteReport card is rendered, THE Collector_Dashboard SHALL display the report's location, wasteType, amount, and createdAt.
3. WHEN a Collector clicks "Mark as Collected" on a WasteReport card, THE System SHALL display a feedback text input field (accepting 1 to 500 characters) before confirming the action.
4. WHEN a Collector submits the "Mark as Collected" action with valid feedback content (1 to 500 characters), THE System SHALL invoke the `collectWaste` server action to update the WasteReport's status to COLLECTED, set the collectorId to the authenticated Collector's id, and create a Feedback record linked to the report; upon success, THE System SHALL remove the card from the feed and display a success indication to the Collector.
5. WHEN the `collectWaste` server action is invoked, THE System SHALL verify the authenticated User has role COLLECTOR and status APPROVED before updating any records.
6. IF the `collectWaste` server action is invoked by a User without role COLLECTOR or with any status other than APPROVED, THEN THE System SHALL return an authorization error without modifying any records.
7. IF the pending report feed contains no WasteReports with status PENDING, THEN THE Collector_Dashboard SHALL display an empty state message.
8. IF the `collectWaste` server action fails due to a server or database error, THEN THE System SHALL display an error message to the Collector without modifying any records.

---

### Requirement 8: Admin Dashboard — Manage Users

**User Story:** As an Admin, I want to view and approve pending Collector accounts, so that only vetted Collectors can access the collection workflow.

#### Acceptance Criteria

1. THE Admin_Dashboard SHALL display a list of all Users with role COLLECTOR and status PENDING, showing each Collector's name, email, and an "Approve" button.
2. WHEN an Admin clicks "Approve" on a pending Collector, THE System SHALL invoke the `updateCollectorStatus` server action to update the User's status to APPROVED; upon success, THE System SHALL remove the Collector from the pending list and display a success indication to the Admin.
3. WHEN the `updateCollectorStatus` server action is invoked, THE System SHALL verify the authenticated User has role ADMIN before updating any records.
4. IF the `updateCollectorStatus` server action is invoked by a User without role ADMIN, THEN THE System SHALL return an authorization error without modifying any records.
5. IF the `updateCollectorStatus` server action fails due to a server or database error, THEN THE System SHALL display an error message to the Admin without modifying any records.
6. IF the pending Collector list is empty, THEN THE Admin_Dashboard SHALL display an empty state message.

---

### Requirement 9: Admin Dashboard — Verify Collections

**User Story:** As an Admin, I want to verify collected waste reports and award points to Collectors, so that the integrity of the collection workflow is maintained and participation is rewarded.

#### Acceptance Criteria

1. THE Admin_Dashboard SHALL display a list of all WasteReports with status COLLECTED, showing location, wasteType, amount, the Collector's name, and associated Feedback content.
2. WHEN an Admin clicks "Verify" on a collected WasteReport, THE System SHALL atomically invoke the `verifyCollection` server action to update the WasteReport's status to VERIFIED and increment the Collector's points by 20 in the same transaction; upon success, THE System SHALL display a success indication to the Admin.
3. WHEN the `verifyCollection` server action is invoked, THE System SHALL verify the authenticated User has role ADMIN before updating any records.
4. IF the `verifyCollection` server action is invoked by a User without role ADMIN, THEN THE System SHALL return an authorization error without modifying any records.
5. IF the `verifyCollection` server action is invoked on a WasteReport that already has status VERIFIED, THEN THE System SHALL return an error without modifying any records.
6. IF the `verifyCollection` server action fails due to a server or database error, THEN THE System SHALL display an error message to the Admin without creating a partial update to the WasteReport status or Collector points.
7. IF the collected report list is empty, THEN THE Admin_Dashboard SHALL display an empty state message.

---

### Requirement 10: Leaderboard

**User Story:** As a user, I want to view a leaderboard of top participants, so that I can see how my contributions compare to others and feel motivated to participate.

#### Acceptance Criteria

1. WHEN an authenticated User with role REPORTER or COLLECTOR accesses the Leaderboard page, THE System SHALL allow access and render the leaderboard.
2. WHEN an authenticated User without role REPORTER or COLLECTOR attempts to access the Leaderboard page, THE System SHALL redirect the User to their appropriate dashboard.
3. THE Leaderboard_Page SHALL display a ranked list of up to 50 Users ordered by points in descending order, showing each User's rank number, name, role, and points.
4. THE Leaderboard_Page SHALL apply a visually distinct style to the authenticated User's own entry in the list to differentiate it from other entries.
5. IF the authenticated User's entry falls outside the top 50, THE Leaderboard_Page SHALL display the authenticated User's rank, name, role, and points in a separate section below the ranked list.
6. IF no Users have earned any points, THE Leaderboard_Page SHALL display an empty state message.
7. THE Leaderboard_Page SHALL use Shadcn_UI components and apply the emerald brand color.

---

### Requirement 11: Profile Page

**User Story:** As a user, I want to view my profile, so that I can see my account details and accumulated points.

#### Acceptance Criteria

1. WHEN an authenticated User with role REPORTER or COLLECTOR accesses the Profile page, THE System SHALL allow access and render the profile.
2. WHEN an authenticated User with role ADMIN or an unauthenticated visitor attempts to access the Profile page, THE System SHALL redirect the User to their appropriate dashboard or the login page respectively.
3. WHEN the Profile page is rendered, THE System SHALL display the authenticated User's name, email, role, status, and points as a numeric value.
4. THE Profile_Page SHALL use Shadcn_UI components and apply the emerald brand color.

---

### Requirement 12: Waiting for Approval Page

**User Story:** As a pending Collector, I want to see a clear status page after registration, so that I understand my account is under review and I cannot yet access the collection workflow.

#### Acceptance Criteria

1. WHEN a User with role COLLECTOR and status PENDING attempts to access any protected route other than the `/pending-approval` page, THE System SHALL redirect the User to the `/pending-approval` page.
2. THE Waiting_For_Approval_Page SHALL display a message indicating that the account is under review and that access will be granted once an Admin approves the account.
3. WHEN the User activates the logout option on the Waiting_For_Approval_Page, THE System SHALL terminate the User's session and redirect the User to the `/login` page.
4. THE Waiting_For_Approval_Page SHALL be built using Shadcn_UI components and SHALL apply the emerald brand color to primary visual elements including headings and the logout button.

---

### Requirement 13: Server Actions Authorization

**User Story:** As a system operator, I want all server actions to enforce role-based authorization, so that no user can perform actions outside their permitted role.

#### Acceptance Criteria

1. IF the `submitReport` server action is invoked with a non-expired, present session where the User has role REPORTER, THEN THE System SHALL proceed to create the WasteReport record; otherwise THE System SHALL return an error without modifying any records.
2. IF the `collectWaste` server action is invoked with a non-expired, present session where the User has role COLLECTOR and status APPROVED, THEN THE System SHALL proceed to update the WasteReport record; otherwise THE System SHALL return an error without modifying any records.
3. IF the `updateCollectorStatus` server action is invoked with a non-expired, present session where the User has role ADMIN, THEN THE System SHALL proceed to update the User status record; otherwise THE System SHALL return an error without modifying any records.
4. IF the `verifyCollection` server action is invoked with a non-expired, present session where the User has role ADMIN, THEN THE System SHALL proceed to update the WasteReport status and Collector points; otherwise THE System SHALL return an error without modifying any records.
5. IF any server action is invoked without a valid authenticated session (session absent or expired), THEN THE System SHALL return an authentication error without modifying any records.
6. IF any server action is invoked with a valid session but the User's role does not match the required role for that action, THEN THE System SHALL return an authorization error without modifying any records.

---

### Requirement 14: UI Consistency and Design System

**User Story:** As a user, I want a visually consistent interface, so that the application feels cohesive and professional across all pages.

#### Acceptance Criteria

1. THE System SHALL use emerald as the primary brand color across all pages and components, applied to headings, buttons, active states, and interactive accents.
2. THE System SHALL use white and Tailwind CSS gray-scale shades (gray-50 through gray-200) as the supporting color palette for backgrounds and body text.
3. THE System SHALL use Shadcn_UI components for all interactive and layout UI elements, including but not limited to buttons, forms, cards, tables, dialogs, and navigation elements.
4. THE System SHALL apply responsive layout breakpoints such that all pages are fully usable at desktop widths (≥1024px) and mobile widths (≤640px), with no horizontal overflow or overlapping elements at either breakpoint.
5. IF the complete UI structure for all pages has not been built and visually validated, THEN THE System SHALL not connect any backend server actions or live database queries to those pages.
