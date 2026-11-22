# Covers: SPEC-000-AC1..AC<n>
# KB: domain/capabilities/<cap>.md, domain/rules/<rule-id>.md
# Designed by: scenario-designer. Levels set by: test-strategist.

@cap:<domain>.<capability>
Feature: <Business capability in plain words>
  As a <role from domain/roles.md>
  I want <goal>
  So that <business value>

  Background:
    Given <shared precondition in business words>

  # Technique: equivalence partition (valid)
  @req:SPEC-000-AC1 @level:<level> @risk:<tier> @suite:regression
  Scenario: <one behaviour, outcome in the title>
    Given <state of the world>
    When <one action>
    Then <observable business outcome>

  # Technique: boundary values from rule <RULE-ID>
  @req:SPEC-000-AC2 @level:<level> @risk:<tier> @suite:regression
  Scenario Outline: <rule name> at its boundaries
    Given <entity> with <attribute> <value>
    When <action>
    Then the result is <result>

    Examples:
      | value     | result   |
      | <min - 1> | rejected |
      | <min>     | accepted |
      | <max>     | accepted |
      | <max + 1> | rejected |

  # Technique: negative / permission (roles.md)
  @req:SPEC-000-AC3 @level:<level> @risk:<tier> @suite:regression
  Scenario: <role> cannot <action>
    Given I am signed in as <role without permission>
    When <action>
    Then the request is denied
    And no <side effect> happens
