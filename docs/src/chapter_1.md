# Part 1: Feasibility

### Background

We've been tasked with designing a Learning Management System (LMS) to manage high school student information and courses.

**Core Features:**
- Account creation and authentication
- Course subscription system based on grade and subject

**Non-Functional Requirements:**
- Secure, scalable, and maintainable infrastructure

**Team**
- Faceman Peck (Front-end developer)
- Hannibal Smith (Back-end developer #1)
- B.A. Baracus (Back-end developer #1)
- Murdock (Junior Full-stack developer)

### Feasibility Assessment

1. Timeline Expectations (if only 1-2 days):

Completing a barebones user interface with little to some functionality in 1-2 days is possible, but completing an MVP (Minimum Viable Product) in 1-2 days may be unrealistic.
The plan below assumes that I could successfully twist the CEO's arm for another day, so our appetite for this project is 3 days.

2. Shape the Work

*(Inspired by [Shape Up](https://basecamp.com/shapeup))*

Solution to be built:
   - A single page for login/signup
   - A course dashboard with clickable subscription actions
   - An API to retrieve and manage course enrollments

Work Sequence:
- Build and integrate authentication
- Create a single end-to-end flow for subscribing to one course
- Expand to cover all predefined courses

Mitigate risks of not meeting timeline:
- Predefine course categories and a simple UI for subscription, no dynamic course creation
- Use an established library for authentication to eliminate rabbit holes
- Solve Unknowns First: Finalize decisions on framework selection, authentication library and database schemas

