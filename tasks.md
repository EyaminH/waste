# Implementation Plan: AI Waste Management System

## Overview

This implementation plan covers building a full-stack Next.js 14 application with role-based access control, waste reporting, collection workflows, and an admin verification system. The application uses TypeScript, Prisma ORM with Neon PostgreSQL, BetterAuth for authentication, and Shadcn UI components with Tailwind CSS.

The implementation follows an incremental approach: database setup → authentication → middleware protection → UI components → role-specific features → testing.

## Tasks

- [x] 1. Initialize project and configure dependencies
  - Create Next.js 14 project with TypeScript and App Router
  - Install and configure Tailwind CSS
  - Install Shadcn UI and initialize component library
  - Install Prisma, BetterAuth, and other core dependencies
  - Configure environment variables for Neon PostgreSQL connection
  - _Requirements: 1.6, 14.3_

- [x] 2. Set up database schema and migrations
  - [x] 2.1 Define Prisma schema with User, WasteReport, and Feedback models
    - Create enums: Role, UserStatus, WasteType, ReportStatus
    - Define User model with all fields, constraints, and indexes
    - Define WasteReport model with relations and indexes
    - Define Feedback model with one-to-one relation to WasteReport
    - Configure referential integrity and cascade rules
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [ ]* 2.2 Write property test for database schema constraints
    - **Property 1: Registration Input Validation Rejects Invalid Data**
    - **Validates: Requirements 2.2**

  - [x] 2.3 Create and run initial Prisma migration
    - Generate migration files
    - Apply migration to Neon database
    - Create Prisma client singleton in lib/prisma.ts
    - _Requirements: 1.6_

- [x] 3. Configure authentication with BetterAuth
  - [x] 3.1 Set up BetterAuth configuration
    - Create lib/auth.ts with BetterAuth configuration
    - Configure session management with role and status in payload
    - Set up password hashing
    - Configure session cookie settings
    - _Requirements: 2.5, 2.6, 2.7_

  - [x] 3.2 Create registration server action
    - Implement user registration with email, name, password, role validation
    - Set status to PENDING for COLLECTOR, APPROVED for REPORTER/ADMIN
    - Hash password using BetterAuth
    - Handle duplicate email errors
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.8_

  - [ ]* 3.3 Write unit tests for registration edge cases
    - Test duplicate email rejection
    - Test status assignment for different roles
    - Test password hashing
    - _Requirements: 2.2, 2.3, 2.4, 2.8_

  - [-] 3.4 Create login and logout server actions
    - Implement login with credential validation
    - Create session with role and status in payload
    - Implement logout with session invalidation
    - Handle invalid credentials errors
    - _Requirements: 2.5, 2.6, 2.9_

- [~] 4. Checkpoint - Verify authentication setup
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement middleware for route protection
  - [-] 5.1 Create middleware.ts with role-based access control
    - Read session from BetterAuth
    - Implement route protection for /dashboard/reporter/*
    - Implement route protection for /dashboard/collector/*
    - Implement route protection for /admin/*
    - Redirect pending collectors to /pending-approval
    - Redirect unauthenticated users to /login
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

  - [ ]* 5.2 Write integration tests for middleware protection
    - Test all role/status combinations with protected routes
    - Test redirect behavior for unauthorized access
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

- [ ] 6. Build core UI components with Shadcn UI
  - [ ] 6.1 Install and configure Shadcn UI base components
    - Install Button, Card, Input, Select, Table, Badge components
    - Configure emerald as primary brand color in Tailwind config
    - Set up typography and spacing tokens
    - _Requirements: 14.1, 14.2, 14.3_

  - [~] 6.2 Create Sidebar component
    - Implement role-specific navigation links
    - Display user name and role
    - Add logout action
    - Apply active state styling to current route
    - Make responsive for mobile and desktop
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

  - [~] 6.3 Create WasteGallery component
    - Create cards for all 5 waste types (ORGANIC, PLASTIC, METAL, E_WASTE, HAZARDOUS)
    - Add descriptions (min 20 characters) for each type
    - Use Shadcn Card components
    - Apply emerald brand color
    - _Requirements: 4.2, 4.3, 4.5, 4.6_

  - [~] 6.4 Create ReportForm component
    - Build form with location, wasteType, amount fields
    - Implement client-side validation
    - Add loading and error states
    - Use Shadcn Input and Select components
    - _Requirements: 6.1, 6.3_

  - [~] 6.5 Create ReportCard component
    - Display report details (location, wasteType, amount, status, createdAt)
    - Show reporter/collector names when available
    - Display feedback content when present
    - Add status badge with color coding
    - Support optional action buttons slot
    - _Requirements: 6.4, 7.2_

  - [~] 6.6 Create LeaderboardTable component
    - Display ranked list of users with rank, name, role, points
    - Highlight current user's entry
    - Show current user separately if outside top 50
    - Limit display to 50 users
    - Handle empty state
    - _Requirements: 10.3, 10.4, 10.5, 10.6_

- [~] 7. Checkpoint - Verify UI components render correctly
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Build authentication pages
  - [~] 8.1 Create registration page (app/(auth)/register/page.tsx)
    - Build registration form with email, name, password, role fields
    - Connect to registration server action
    - Display validation errors
    - Redirect to appropriate dashboard on success
    - Add navigation link to login page
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [~] 8.2 Create login page (app/(auth)/login/page.tsx)
    - Build login form with email and password fields
    - Connect to login server action
    - Display authentication errors
    - Redirect to appropriate dashboard on success
    - Add navigation link to registration page
    - _Requirements: 2.5, 2.9_

  - [~] 8.3 Create pending approval page (app/pending-approval/page.tsx)
    - Display waiting message for pending collectors
    - Add logout button
    - Use Shadcn UI components with emerald branding
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

- [ ] 9. Build landing page
  - [~] 9.1 Create landing page (app/page.tsx)
    - Render WasteGallery component
    - Add navigation links to login and register pages
    - Apply emerald brand color to headings and buttons
    - Make responsive for mobile and desktop
    - Add error boundary for graceful error handling
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

- [ ] 10. Implement Reporter features
  - [~] 10.1 Create submitReport server action
    - Validate session (must be REPORTER role)
    - Validate input fields (location, wasteType, amount)
    - Execute transaction: create WasteReport + increment reporter points by 10
    - Return success or error response
    - _Requirements: 6.2, 13.1_

  - [ ]* 10.2 Write property test for report submission transaction
    - **Property 2: Waste Report Submission Transaction Integrity**
    - **Validates: Requirements 6.2**

  - [ ]* 10.3 Write property test for report validation
    - **Property 3: Waste Report Validation Rejects Invalid Data**
    - **Validates: Requirements 6.3**

  - [~] 10.4 Create Reporter report submission page (app/dashboard/reporter/report/page.tsx)
    - Render ReportForm component
    - Connect to submitReport server action
    - Display success/error feedback
    - Show list of reporter's past submissions
    - Order reports by createdAt descending
    - Handle empty state
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

  - [ ]* 10.5 Write property test for report list ordering
    - **Property 4: Reporter's Report List Ordering**
    - **Validates: Requirements 6.4**

  - [~] 10.6 Create Reporter profile page (app/dashboard/reporter/profile/page.tsx)
    - Display user name, email, role, status, points
    - Use Shadcn UI components with emerald branding
    - _Requirements: 11.1, 11.3, 11.4_

  - [~] 10.7 Create Reporter leaderboard page (app/dashboard/reporter/leaderboard/page.tsx)
    - Fetch top 50 users ordered by points descending
    - Render LeaderboardTable component
    - Highlight current user's entry
    - Show current user separately if outside top 50
    - Handle empty state
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

  - [ ]* 10.8 Write property test for leaderboard ordering
    - **Property 8: Leaderboard Ordering and Limiting**
    - **Validates: Requirements 10.3**

- [~] 11. Checkpoint - Verify Reporter workflow
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement Collector features
  - [~] 12.1 Create collectWaste server action
    - Validate session (must be COLLECTOR with APPROVED status)
    - Validate feedback content (1-500 characters)
    - Execute transaction: update report status to COLLECTED + set collectorId + create Feedback
    - Return success or error response
    - _Requirements: 7.4, 7.5, 7.6, 13.2_

  - [ ]* 12.2 Write property test for collection transaction
    - **Property 5: Collection Transaction Integrity**
    - **Validates: Requirements 7.4**

  - [~] 12.3 Create Collector collect page (app/dashboard/collector/collect/page.tsx)
    - Fetch all WasteReports with status PENDING
    - Render ReportCard for each pending report
    - Add "Mark as Collected" button with feedback input
    - Connect to collectWaste server action
    - Remove collected report from feed on success
    - Handle empty state
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.7, 7.8_

  - [~] 12.4 Create Collector profile page (app/dashboard/collector/profile/page.tsx)
    - Display user name, email, role, status, points
    - Use Shadcn UI components with emerald branding
    - _Requirements: 11.1, 11.3, 11.4_

  - [~] 12.5 Create Collector leaderboard page (app/dashboard/collector/leaderboard/page.tsx)
    - Fetch top 50 users ordered by points descending
    - Render LeaderboardTable component
    - Highlight current user's entry
    - Show current user separately if outside top 50
    - Handle empty state
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

- [~] 13. Checkpoint - Verify Collector workflow
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Implement Admin features
  - [~] 14.1 Create updateCollectorStatus server action
    - Validate session (must be ADMIN role)
    - Update User status to APPROVED
    - Return success or error response
    - _Requirements: 8.2, 8.3, 13.3_

  - [ ]* 14.2 Write property test for collector approval
    - **Property 6: Collector Approval Status Transition**
    - **Validates: Requirements 8.2**

  - [~] 14.3 Create Admin manage users page (app/admin/users/page.tsx)
    - Fetch all Users with role COLLECTOR and status PENDING
    - Display list with name, email, and "Approve" button
    - Connect to updateCollectorStatus server action
    - Remove approved collector from list on success
    - Handle empty state
    - _Requirements: 8.1, 8.2, 8.4, 8.5, 8.6_

  - [~] 14.4 Create verifyCollection server action
    - Validate session (must be ADMIN role)
    - Verify report status is COLLECTED (not already VERIFIED)
    - Execute transaction: update report status to VERIFIED + increment collector points by 20
    - Return success or error response
    - _Requirements: 9.2, 9.3, 9.4, 9.5, 13.4_

  - [ ]* 14.5 Write property test for verification transaction
    - **Property 7: Collection Verification Transaction Integrity**
    - **Validates: Requirements 9.2**

  - [~] 14.6 Create Admin verify reports page (app/admin/verify/page.tsx)
    - Fetch all WasteReports with status COLLECTED
    - Display list with location, wasteType, amount, collector name, feedback
    - Add "Verify" button for each report
    - Connect to verifyCollection server action
    - Display success feedback on verification
    - Handle empty state
    - _Requirements: 9.1, 9.2, 9.6, 9.7_

- [~] 15. Checkpoint - Verify Admin workflow
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Implement server action authorization enforcement
  - [~] 16.1 Add authorization checks to all server actions
    - Verify session exists and is not expired
    - Verify user role matches required role for each action
    - Return authentication/authorization errors without modifying data
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_

  - [ ]* 16.2 Write property test for authorization enforcement
    - **Property 9: Server Action Authorization Enforcement**
    - **Validates: Requirements 13.5, 13.6**

- [ ] 17. Add responsive design and UI polish
  - [~] 17.1 Implement responsive layouts for all pages
    - Test all pages at mobile (≤640px) and desktop (≥1024px) breakpoints
    - Ensure no horizontal overflow or overlapping elements
    - Make Sidebar responsive (collapsible on mobile)
    - _Requirements: 14.4_

  - [~] 17.2 Apply consistent emerald branding across all pages
    - Verify emerald color on headings, buttons, active states
    - Verify white and gray-scale backgrounds and text
    - Ensure all Shadcn UI components use consistent theming
    - _Requirements: 14.1, 14.2, 14.3_

- [ ] 18. Set up testing infrastructure
  - [~] 18.1 Configure Vitest for unit and property tests
    - Install Vitest and fast-check
    - Configure test database (in-memory SQLite or test Neon instance)
    - Set up test utilities for user creation and cleanup
    - Configure test coverage reporting
    - _Requirements: All property tests_

  - [~] 18.2 Create test utilities and helpers
    - Create createTestUser helper
    - Create cleanupTestData helper
    - Create mock session helpers
    - Create database seeding utilities
    - _Requirements: All property tests_

- [ ] 19. Write property-based tests
  - [ ]* 19.1 Implement all 9 property tests
    - Property 1: Registration validation
    - Property 2: Report submission transaction
    - Property 3: Report validation
    - Property 4: Report list ordering
    - Property 5: Collection transaction
    - Property 6: Collector approval
    - Property 7: Verification transaction
    - Property 8: Leaderboard ordering
    - Property 9: Authorization enforcement
    - Run each test with minimum 100 iterations
    - Tag each test with feature name and property number
    - _Requirements: All correctness properties_

- [ ]* 20. Write integration tests
  - [ ]* 20.1 Write database constraint integration tests
    - Test unique email constraint
    - Test foreign key constraints
    - Test cascade delete behavior
    - _Requirements: 1.4, 1.5_

  - [ ]* 20.2 Write authentication flow integration tests
    - Test registration → login → session creation
    - Test logout → session invalidation
    - Test middleware + server action authorization
    - _Requirements: 2.5, 2.6, 3.1-3.8_

  - [ ]* 20.3 Write transaction integrity integration tests
    - Test report submission transaction rollback on failure
    - Test collection transaction rollback on failure
    - Test verification transaction rollback on failure
    - _Requirements: 6.2, 7.4, 9.2_

- [ ] 21. Final checkpoint and deployment preparation
  - [~] 21.1 Run all tests and verify coverage
    - Run all property tests (100+ iterations each)
    - Run all unit tests
    - Run all integration tests
    - Verify coverage meets goals (80%+ for server actions)
    - _Requirements: All_

  - [~] 21.2 Create root layout with Sidebar integration
    - Create app/layout.tsx with global styles
    - Conditionally render Sidebar for authenticated routes
    - Add error boundary for global error handling
    - Configure metadata and fonts
    - _Requirements: 5.1, 14.3_

  - [~] 21.3 Verify all requirements are implemented
    - Review requirements document
    - Verify all acceptance criteria are met
    - Test all user workflows end-to-end manually
    - Document any known issues or limitations
    - _Requirements: All_

  - [~] 21.4 Prepare for deployment
    - Set up production environment variables
    - Configure Neon database for production
    - Run production build and verify no errors
    - Create deployment documentation
    - _Requirements: All_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation and provide opportunities for user feedback
- Property tests validate universal correctness properties with 100+ iterations
- Unit and integration tests validate specific examples and edge cases
- The implementation follows a bottom-up approach: infrastructure → authentication → UI → features → testing
- All server actions must enforce role-based authorization before modifying data
- All database transactions must be atomic (all operations succeed or all fail)
- All UI components must use Shadcn UI with emerald brand color
- All pages must be responsive at mobile (≤640px) and desktop (≥1024px) breakpoints

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["2.1", "3.1"] },
    { "id": 2, "tasks": ["2.2", "2.3", "3.2"] },
    { "id": 3, "tasks": ["3.3", "3.4", "5.1", "6.1"] },
    { "id": 4, "tasks": ["5.2", "6.2", "6.3", "6.4", "6.5", "6.6"] },
    { "id": 5, "tasks": ["8.1", "8.2", "8.3", "9.1"] },
    { "id": 6, "tasks": ["10.1"] },
    { "id": 7, "tasks": ["10.2", "10.3", "10.4"] },
    { "id": 8, "tasks": ["10.5", "10.6", "10.7"] },
    { "id": 9, "tasks": ["10.8", "12.1"] },
    { "id": 10, "tasks": ["12.2", "12.3", "12.4", "12.5"] },
    { "id": 11, "tasks": ["14.1"] },
    { "id": 12, "tasks": ["14.2", "14.3", "14.4"] },
    { "id": 13, "tasks": ["14.5", "14.6", "16.1"] },
    { "id": 14, "tasks": ["16.2", "17.1", "17.2"] },
    { "id": 15, "tasks": ["18.1", "18.2"] },
    { "id": 16, "tasks": ["19.1", "20.1", "20.2", "20.3"] },
    { "id": 17, "tasks": ["21.1", "21.2"] },
    { "id": 18, "tasks": ["21.3", "21.4"] }
  ]
}
```
