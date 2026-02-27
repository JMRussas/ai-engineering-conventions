# Test-First with AI

## What

Write failing tests that describe the behavior you want *before* asking the AI to implement the feature or fix. The tests become a precise, executable specification that constrains the AI's solution space and provides immediate validation.

## Why

Without test-first:
- **The AI's solution is unconstrained.** It has infinite degrees of freedom and picks an approach that may not match what you actually wanted.
- **Validation is manual.** You have to read the code carefully to determine if it's correct, which is slow and error-prone.
- **Requirements are ambiguous.** Natural language descriptions of behavior have gaps. Tests force you to be precise about inputs, outputs, and edge cases.

Test-first with AI is more powerful than test-first with humans because the AI can iterate to green much faster — the feedback loop is seconds, not minutes.

## How

### The workflow

1. **Write the test(s).** Describe the behavior you want in test form. Don't write the implementation.
2. **Show the AI the failing tests.** "Here are failing tests. Implement the code to make them pass."
3. **AI implements.** The tests constrain the solution — the AI can't drift into a different design.
4. **Tests pass → done.** Or if they don't, the AI iterates automatically.

### What makes good AI-constraining tests

- **Test behavior, not implementation.** "Given X input, expect Y output" — not "call method Z with parameter W."
- **Include edge cases.** The AI handles happy paths well. It's the edges where it cuts corners.
- **Test error conditions.** "When input is invalid, raise ValueError" — without this test, the AI might silently return None.
- **Keep tests readable.** The AI uses them as a spec. Clear test names and assertions help it understand intent.

### When to write tests after (and that's OK)

- **Exploratory work** — you don't know what the interface should look like yet
- **UI/visual work** — hard to test-first (but you can test-first the logic layer)
- **Bug fixes** — sometimes you need to find the bug before you can write a test for it (but do write the test before fixing)

## Example

**You write:**
```python
def test_parse_duration_seconds():
    assert parse_duration("30s") == 30

def test_parse_duration_minutes():
    assert parse_duration("5m") == 300

def test_parse_duration_hours():
    assert parse_duration("2h") == 7200

def test_parse_duration_combined():
    assert parse_duration("1h30m") == 5400

def test_parse_duration_invalid():
    with pytest.raises(ValueError, match="Invalid duration"):
        parse_duration("abc")

def test_parse_duration_negative():
    with pytest.raises(ValueError, match="must be positive"):
        parse_duration("-5m")
```

**You tell the AI:**
"Implement `parse_duration` in `utils/time.py` to make these tests pass."

**What you get:** A function that handles exactly the cases you specified, with the exact error messages you want, and provably works because the tests pass.

**Compare to:** "Write a function that parses duration strings like '30s', '5m', '2h'" — the AI might miss the combined format, might not raise on invalid input, might use different error messages.

## When to skip

- **Trivial changes** where the test would be more complex than the code (e.g., renaming a variable).
- **Prototype/spike work** where you're exploring possibilities, not building to spec.
- **Infrastructure/config changes** that are hard to unit test (but consider integration tests).
