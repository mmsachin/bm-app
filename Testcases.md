## Test Cases for Budget Management Chatbot

| No. | Category          | Command to Copy                                                                                                    | Expected Result                                          |
|-----|-------------------|--------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| 1   | User Management   | `add user ldap john123 first name John last name Doe email john@example.com level 5`                              | User John created successfully                             |
| 2   | User Management   | `add user ldap alice345 first name Alice last name Smith email alice@example.com level 4`                             | User Alice created successfully                            |
| 3   | User Management   | `add user ldap bob789 first name Bob last name Wilson email bob@example.com level 3`                               | User Bob created successfully                              |
| 4   | User Management   | `add user ldap sarah567 first name Sarah last name Johnson email sarah@example.com level 3`                             | User Sarah created successfully                            |
| 5   | User Management   | `add user ldap mike789 first name Mike last name Brown email mike@example.com level 2`                               | User Mike created successfully                             |
| 6   | View Users        | `list users`                                                                                                        | Shows all created users                                     |
| 7   | Organization      | `show me my organization as john123`                                                                               | Shows John's org structure                                 |
| 8   | Organization      | `show me my organization as alice345`                                                                               | Shows Alice's org structure                                |
| 9   | AOP Creation      | `add aop name "FY2024 Operations" amount 1000000`                                                                    | AOP created with ID 1                                     |
| 10  | AOP Creation      | `add aop name "FY2024 Marketing" amount 500000`                                                                     | AOP created with ID 2                                     |
| 11  | AOP Creation      | `add aop name "FY2024 IT Projects" amount 750000`                                                                  | AOP created with ID 3                                     |
| 12  | View AOPs         | `list aops`                                                                                                         | Shows all created AOPs                                    |
| 13  | Budget Creation   | `add budget aop 1 amount 250000 project "Infrastructure Upgrade"`                                                   | Budget created successfully                                |
| 14  | Budget Creation   | `add budget aop 1 amount 150000 project "Security Implementation"`                                                    | Budget created successfully                                |
| 15  | Budget Creation   | `add budget aop 2 amount 200000 project "Digital Marketing Campaign"`                                                | Budget created successfully                                |
| 16  | Budget Creation   | `add budget aop 2 amount 150000 project "Brand Redesign"`                                                            | Budget created successfully                                |
| 17  | Budget Creation   | `add budget aop 3 amount 300000 project "AI Integration"`                                                            | Budget created successfully                                |
| 18  | Error Testing     | `add user ldap john123 first name John last name Doe email john@example.com level 5`                              | Should fail (duplicate user)                             |
| 19  | Error Testing     | `add budget aop 999 amount 50000 project "Non-existent AOP"`                                                        | Should fail (invalid AOP)                                 |
| 20  | Help              | `help`                                                                                                          | Shows available commands                                    |

<br>

**Testing Order:**

1.  Run test cases 1-5 to create users
2.  Run test case 6 to verify users
3.  Run test cases 7-8 to check organization structure
4.  Run test cases 9-11 to create AOPs
5.  Run test case 12 to verify AOPs
6.  Run test cases 13-17 to create budgets
7.  Run test cases 18-19 to verify error handling
8.  Run test case 20 to check help system

<br>

**Tips:**

*   Copy each command exactly as shown
*   Check responses after each command
*   Note the IDs returned when creating AOPs
*   Verify error messages are clear and helpful
