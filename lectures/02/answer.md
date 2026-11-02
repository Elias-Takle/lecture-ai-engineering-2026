## Homework

### 1. Chosen Level

**Basic — LoRA Rank Comparison**

### 2. Objective

The objective of this experiment was to investigate how changing the LoRA rank from 16 to 8 affects the fine-tuning performance of the Qwen3.5-0.8B model.

I compared the two experiments using four measurements:

- Format rate after training
- Content rate after training
- Final training loss
- Training time

The purpose was to understand whether reducing the LoRA rank could maintain model performance while reducing training cost.

### 3. Experimental Settings

I used the `Qwen/Qwen3.5-0.8B` base model and the LoRA fine-tuning method without quantization.

I changed only one parameter: the LoRA rank.

| Parameter | Original experiment | Modified experiment |
|---|---:|---:|
| Base model | Qwen3.5-0.8B | Qwen3.5-0.8B |
| LoRA rank (`lora_r`) | 16 | 8 |
| Learning rate (`lr`) | 0.0002 | 0.0002 |
| Training epochs | 20 | 20 |
| LoRA alpha | 32 | 32 |
| Warmup steps | 6 | 6 |
| Random seed | 42 | 42 |
| Maximum sequence length | 512 | 512 |
| Maximum new tokens | 96 | 96 |
| Quantization | None | None |

The dataset, evaluation questions, base model revision, and other configuration settings were kept unchanged. After modifying the LoRA rank, I restarted the runtime and executed the notebook again from the beginning.

### 4. Experimental Results

I compared the two `result.json` files and recorded the final training loss and training time from the training outputs.

| Metric | Original (r=16) | Modified (r=8) |
|---|---:|---:|
| Format rate after training | 100% | 100% |
| Content rate after training | 90.48% | 90.48% |
| Final training loss | 0.014880 | 0.014616 |
| Training time | 198 seconds | 188 seconds |

### 5. Discussion and Comparison

#### 5.1 Format Rate

Both experiments achieved a format rate of 100% after training.

This means that both LoRA configurations successfully produced outputs that satisfied the required output format in all 21 evaluation questions.

Reducing the LoRA rank from 16 to 8 did not reduce format compliance in this experiment.

**Observation: Unchanged performance.**

#### 5.2 Content Rate

Both experiments achieved a content rate of 90.48%.

This indicates that reducing the LoRA rank did not change the measured content accuracy on the evaluation dataset.

Although the two configurations had different LoRA ranks, they achieved the same content evaluation result.

**Observation: Unchanged performance.**

#### 5.3 Final Training Loss

The original experiment with rank 16 achieved a final training loss of 0.014880, while the modified experiment with rank 8 achieved 0.014616.

The rank-8 experiment therefore had a slightly lower final training loss.

The difference was:

0.014880 - 0.014616 = 0.000264

This is a small difference. It suggests that the rank-8 model fitted the training data slightly better according to this particular training-loss measurement.

However, training loss alone does not determine which model performs better on unseen data. In this experiment, both configurations achieved exactly the same format and content rates on the evaluation set.

**Observation: Slight improvement in training loss for r=8.**

#### 5.4 Training Time

The rank-16 experiment took 198 seconds, while the rank-8 experiment took 188 seconds.

The time difference was:

198 - 188 = 10 seconds

The rank-8 experiment was approximately 5.05% faster than the rank-16 experiment.

This is consistent with the idea that a lower LoRA rank can reduce the amount of trainable adapter parameters and computational work.

However, training time can also be affected by GPU utilization, runtime conditions, and other system factors. Therefore, this single experiment does not prove that reducing the rank will always produce the same time saving.

**Observation: Training time improved by 10 seconds.**

#### 5.5 Summary of Improvements, Regressions, and Unchanged Results

| Category | Result | Explanation |
|---|---|---|
| Improved | Final training loss | Decreased slightly from 0.014880 to 0.014616. |
| Improved | Training time | Decreased from 198 to 188 seconds. |
| Unchanged | Format rate | Both achieved 100%. |
| Unchanged | Content rate | Both achieved 90.48%. |
| Worsened | None observed | No reduction in the measured evaluation rates. |

The two experiments also recorded zero regressed evaluation questions after training.

Overall, reducing the LoRA rank from 16 to 8 maintained the measured evaluation performance while producing a slightly lower final training loss and a shorter training time.

### 6. When Fine-Tuning Is Useful

Fine-tuning is useful when a model needs to learn a consistent behavior, response style, or output structure from examples.

For example, in this exercise, the model was expected to produce structured responses following a specific format. Fine-tuning helped improve the format rate from approximately 95.24% before training to 100% after training.

It also improved the content rate from approximately 38.10% before training to 90.48% after training.

This demonstrates that fine-tuning can be useful when:

- A model needs to follow a consistent output format, such as JSON.
- An application requires a particular response style or behavior.
- There are enough high-quality examples demonstrating the desired behavior.
- Repeated tasks require consistent responses.
- The model needs to adapt to a specific task or domain.

For example, a customer-support application could use fine-tuning to make responses follow a consistent structure and communication style.

### 7. When Fine-Tuning Is Not Useful

Fine-tuning is not always the best solution for every problem.

It is not necessarily useful when the main requirement is to provide information that changes frequently or is not available in the training dataset.

For example, if a university chatbot is asked about a newly announced examination date, fine-tuning alone cannot guarantee that the model knows the latest information.

Fine-tuning also does not guarantee that a model will always provide factually correct answers or avoid making unsupported claims.

It may be less suitable when:

- The required information changes frequently.
- The application needs access to current external information.
- The knowledge is not included in the training examples.
- There are too few high-quality training examples.
- A simpler approach, such as prompt engineering or retrieval-augmented generation (RAG), can solve the problem more effectively.

For example, a university chatbot could use RAG to retrieve the latest information from official university documents before generating an answer. This makes it easier to update information without repeatedly fine-tuning the model.

Therefore, fine-tuning is more appropriate for teaching a model how to respond, while retrieval is often more appropriate for providing information from changing or external sources. These approaches can also be combined.

### 8. Conclusion

In this homework, I investigated the effect of reducing the LoRA rank from 16 to 8 while keeping the other experimental settings unchanged.

The results showed that both configurations achieved a 100% format rate and a 90.48% content rate after training. The rank-8 experiment achieved a slightly lower final training loss of 0.014616 compared with 0.014880 for rank 16. It also reduced training time from 198 seconds to 188 seconds.

Based on these results, rank 8 maintained the measured evaluation performance while requiring less training time in this experiment.

However, I cannot conclude that rank 8 is universally better than rank 16 based on only these two experiments. Additional experiments using different datasets, random seeds, and evaluation questions would be necessary to establish whether this result generalizes.

The experiment helped me understand that LoRA rank affects the capacity of the trainable adapter, and that a higher rank does not automatically guarantee better evaluation performance.

### 9. Verification and Use of AI Assistance

I used AI assistance to understand the concepts, plan the comparison, and organize the discussion of the experimental results.

I personally executed the original rank-16 experiment and the modified rank-8 experiment, changed the LoRA rank, and compared the generated `result.json` files and training outputs.

The reported evaluation metrics were taken from the experiment results, while the final training loss and training time were taken from the training outputs.