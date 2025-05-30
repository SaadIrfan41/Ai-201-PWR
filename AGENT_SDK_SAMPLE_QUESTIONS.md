
---

### ✅ **QUIZ: Fundamentals of Agentic AI**

**Total Questions: 48 | Duration: 120 Minutes | Format: MCQ**

---

#### 🧠 **Section 1: Core Concepts of the OpenAI Agents SDK (12 questions)**

1. What is the primary role of `agent.clone()` in the Agents SDK?
   A) Logging
   B) Running async tasks
   C) Cloning a base agent with optional changes
   D) Restarting the runner

2. Why is agent cloning useful in multi-user applications?
   A) Reduces memory usage
   B) Avoids repeated base config and isolates context
   C) Increases token length
   D) Enables live streaming

3. Which function is used to run an agent synchronously?
   A) `Runner.run_async()`
   B) `agent.execute()`
   C) `Runner.run_sync()`
   D) `agent.start()`

4. What is the purpose of `@function_tool`?
   A) Marks a method as async
   B) Registers a function as a callable tool
   C) Streams outputs
   D) Configures a dynamic instruction

5. What does the Agent Loop control?
   A) Python decorators
   B) Markdown generation
   C) LLM interaction, tools, and turn limits
   D) Prompt length

6. What happens when `MaxTurnsExceeded` is raised?
   A) The process is retried
   B) An infinite loop starts
   C) The agent loop stops due to too many turns
   D) Tool execution is canceled

7. What SDK component is used to link one agent’s output to another agent’s input?
   A) Agent loop
   B) Handoff
   C) Cloning
   D) Prompt decorator

8. What does `input_filter` in a Handoff do?
   A) Formats final output
   B) Parses Markdown
   C) Cleans/modifies input before reaching the next agent
   D) Filters invalid tools

9. What can `output_filter` in a Handoff be used for?
   A) Cloning agents
   B) Validating tool inputs
   C) Stripping internal metadata from agent responses
   D) Logging context

10. Which Pydantic feature is used to define expected input/output formats in tools?
    A) Guardrails
    B) Field types and schemas
    C) Decorators
    D) Coroutines

11. What does a `ModelBehaviorError` indicate?
    A) Python syntax error
    B) LLM returned malformed output or called an unknown tool
    C) API rate limit
    D) Pydantic failure

12. What happens if `failure_error_function=None` is set in a tool?
    A) It disables streaming
    B) It forces retries
    C) Tool exceptions are propagated
    D) Tool output is hidden

---

#### 🛠️ **Section 2: Async and Code Execution (10 questions)**

13. What does `async def` define in Python?
    A) A function that runs in a thread
    B) A blocking task
    C) A coroutine
    D) A tool decorator

14. Which function initiates an async Python program?
    A) `asyncio.run()`
    B) `await`
    C) `runner.start()`
    D) `openai.run_async()`

15. What does `await` do?
    A) Starts a thread
    B) Waits for a blocking task
    C) Pauses until an async task completes
    D) Calls a function synchronously

16. What is the purpose of `asyncio.gather()`?
    A) Creates a coroutine
    B) Waits for a single task
    C) Terminates async functions
    D) Runs multiple async tasks concurrently

17. Which statement is true about coroutines?
    A) They block the main thread
    B) They can't be awaited
    C) They support pause/resume
    D) They only work with `@staticmethod`

18. What must wrap the execution of async code in a main function?
    A) `await()`
    B) `run()`
    C) `asyncio.run()`
    D) `tool.run_async()`

19. What is the correct way to define an async tool?
    A) `@function_tool` on a regular function
    B) `@async_tool` decorator
    C) `@function_tool` with `async def`
    D) No decorator is required

20. What ensures an async tool can be paused and resumed?
    A) Synchronous execution
    B) Context Manager
    C) Coroutine behavior
    D) Logging

21. If an error occurs during streaming, what is the SDK's expected behavior?
    A) Shutdown
    B) Raise `TypeError`
    C) Gracefully handle partial output
    D) Retry tool calls

22. What can happen if no error handling is added to a dynamic prompt function?
    A) Safe fallback
    B) Partial execution
    C) Agent failure
    D) Warning only

---

#### 💡 **Section 3: Prompt Engineering and Reasoning (14 questions)**

23. What does Chain-of-Thought prompting enable?
    A) Faster response generation
    B) Parallel reasoning
    C) Step-by-step explanation of reasoning
    D) Tool calling

24. How do you trigger CoT prompting?
    A) Use `@cot_prompt`
    B) Add “Explain your reasoning” in prompt
    C) Set `prompt_type="cot"`
    D) Use filters

25. Why is persona design important in prompting?
    A) Reduces token usage
    B) Changes memory settings
    C) Helps model stay consistent and focused
    D) Affects tool speed

26. Which technique helps maintain tone and accuracy in LLM responses?
    A) Handoffs
    B) Dynamic context
    C) Persona prompting
    D) Pydantic schema

27. What is dynamic instruction prompting?
    A) Static prompts per session
    B) Hardcoded prompts
    C) Instructions that update based on user input or context
    D) Prompts embedded in function docs

28. Why would you use a decorator with a dynamic instruction function?
    A) For async execution
    B) To validate Pydantic output
    C) To modify prompts on-the-fly
    D) To create links

29. What technique avoids sensitive data leaks in LLM output?
    A) Prompt expansion
    B) Chain-of-Thought
    C) Filters
    D) Logging

30. Which Markdown syntax correctly renders a link?
    A) `(url)[label]`
    B) `[label](url)`
    C) `<a href="url">label</a>`
    D) `{link: url}`

31. What is the Markdown syntax for images?
    A) `[img](url)`
    B) `<img src="url" />`
    C) `![alt](url)`
    D) `{image: url}`

32. What is one key goal of prompt engineering?
    A) Enable GPU acceleration
    B) Force tool selection
    C) Improve model output quality
    D) Make code run faster

33. Which is NOT a benefit of CoT prompting?
    A) Enhanced reasoning
    B) Better planning
    C) Accurate tool selection
    D) Shorter output

34. When should you use structured prompting with CoT?
    A) For very short answers
    B) For LLM fine-tuning
    C) For complex decision-making tasks
    D) When output is not JSON

35. What’s a good system message for a financial advisor persona?
    A) “You are helpful.”
    B) “You are a financial expert focused on client budgeting.”
    C) “Hello user.”
    D) “Respond fast.”

36. What does the prompt "You are a travel planner" achieve?
    A) Applies filters
    B) Defines a role and tone
    C) Logs the response
    D) Uses a tool

---

#### ⚠️ **Section 4: Error Handling, Guardrails, and Edge Cases (12 questions)**

37. What error is raised if input violates a constraint?
    A) `ValueError`
    B) `InputGuardrailTripwireTriggered`
    C) `ValidationException`
    D) `PromptLimitExceeded`

38. What error is raised for invalid agent output?
    A) `ModelOutputError`
    B) `ToolException`
    C) `OutputGuardrailTripwireTriggered`
    D) `RunnerFailure`

39. If the LLM returns non-JSON output when JSON is expected, what happens?
    A) SDK ignores the output
    B) ModelBehaviorError is raised
    C) Output is wrapped in a string
    D) Default tool error function is invoked

40. What is the purpose of default\_tool\_error\_function?
    A) Ends the loop
    B) Sends structured error to LLM
    C) Prevents execution
    D) Restarts the tool

41. How can a developer customize tool error handling?
    A) Override default exception class
    B) Use failure\_error\_function
    C) Use `@error_tool`
    D) Edit agent config

42. If `failure_error_function` is not provided, what is the fallback?
    A) SDK logs a warning
    B) A tool retry occurs
    C) The exception is raised and propagated
    D) Output is suppressed

43. How can dynamic instruction functions fail?
    A) Timeout
    B) Schema mismatch
    C) Exception during prompt generation
    D) Corrupted token stream

44. What’s a best practice for guarding dynamic prompt functions?
    A) Use static context
    B) Add try/except to handle failures
    C) Avoid conditionals
    D) Disable tool chaining

45. When does a `GuardrailTripwire` help most?
    A) Prompt formatting
    B) Tool retries
    C) Enforcing input/output constraints
    D) Sending Markdown

46. What does the SDK do if a streaming error occurs mid-response?
    A) Cancels tool
    B) Returns an empty response
    C) Handles gracefully and allows partial output
    D) Shuts down

47. What is the fallback mechanism for malformed tool responses?
    A) Retry
    B) Return error string
    C) Use default\_tool\_error\_function
    D) Run sync

48. What is one common cause of model errors in a tool context?
    A) Wrong Markdown
    B) Incorrect persona
    C) Calling undefined tool or malformed JSON
    D) Exceeding token limit

---

