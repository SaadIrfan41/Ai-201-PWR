# Google Prompt Engineering Guide (Summary)

## I. LLM Output Settings

- **Output Length**: Affects detail level, cost, and processing time.
- **Temperature**: Controls randomness. Lower = predictable, Higher = creative.
- **Top P and Top K Sampling**: Restricts word choices to fine-tune output precision or creativity.

---

## II. Prompting Techniques

- **Zero-shot prompting**: Task description without examples, ideal for simple outputs.
- **One-shot/Few-shot prompting**: Provide 1 or more examples to clarify the desired pattern. Use relevant, high-quality, and diverse examples.

### System, Contextual, and Role Prompting

- **System prompting**: Sets the overall goal or behavior of the AI.
- **Contextual prompting**: Supplies background for better comprehension.
- **Role prompting**: Instructs the AI to adopt a specific persona or style.

---

## III. Advanced Prompting Techniques

- **Stepback prompting**: Start with a broad question, then zoom in for specificity.
- **Chain of thought prompting**: Ask for step-by-step reasoning before the final answer. Improves transparency, but increases cost/time.
- **Self-consistency**: Use a high temperature and repeat the question to gather multiple answers and select the most frequent.
- **Tree of thought**: AI explores multiple solutions before picking the best.
- **Reason and Act (ReAct)**: AI plans, takes actions (like searching), and refines its answer based on new info.
- **Automatic prompt engineering**: AI generates and improves its own prompts.
- **Multimodal prompting**: Combine text with images, audio, or code to give more context.

---

## IV. Best Practices for Beginner Prompt Engineers

- **Keep it simple**: Use clear, direct instructions.
- **Provide examples**: Use one-shot or few-shot prompting to show expected outputs.
- **Be specific about the output**: Define output format like "short answer", "paragraph", or "JSON".
- **Use positive instructions**: Guide the model by stating what to do, not what to avoid.
- **Control max token length**: Limit output size for efficiency.
- **Experiment and iterate**: Adjust prompts, wording, temperature, and formats to improve results.
- **Learn and document**: Track what works, including prompt structure, model settings, and outcomes.

---

> _Prompt engineering is a continual process of refinement, testing, and learning. Even beginners can become proficient with consistent practice._
