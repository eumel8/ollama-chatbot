# Test cases

## Environment

<details>

Operating System

```
# cat /etc/os-release
PRETTY_NAME="Ubuntu 22.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.5 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

Kernel
```
# uname -a
Linux kubeadm-test-kubeadm 5.15.0-131-generic #141-Ubuntu SMP Fri Jan 10 21:18:28 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```

Memory

```
$ lsmem
RANGE                                 SIZE  STATE REMOVABLE  BLOCK
0x0000000000000000-0x00000000bfffffff   3G online       yes   0-23
0x0000000100000000-0x000000043fffffff  13G online       yes 32-135

Memory block size:       128M
Total online memory:      16G
Total offline memory:      0B
```


CPU

```
Architecture:             x86_64
  CPU op-mode(s):         32-bit, 64-bit
  Address sizes:          42 bits physical, 48 bits virtual
  Byte Order:             Little Endian
CPU(s):                   4
  On-line CPU(s) list:    0-3
Vendor ID:                GenuineIntel
  Model name:             Intel(R) Xeon(R) Gold 6151 CPU @ 3.00GHz
    CPU family:           6
    Model:                85
    Thread(s) per core:   2
    Core(s) per socket:   2
    Socket(s):            1
    Stepping:             4
    BogoMIPS:             6000.00
    Flags:                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss
                           ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_fr
                          eq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave
                          avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti ssbd ibrs ibpb stibp fsgsbas
                          e tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm mpx avx512f avx512dq rdseed adx smap clflushop
                          t clwb avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 arat md_clear flush_l1d arch_capabilities
Virtualization features:
  Hypervisor vendor:      KVM
  Virtualization type:    full
Caches (sum of all):
  L1d:                    64 KiB (2 instances)
  L1i:                    64 KiB (2 instances)
  L2:                     2 MiB (2 instances)
  L3:                     24.8 MiB (1 instance)
NUMA:
  NUMA node(s):           1
  NUMA node0 CPU(s):      0-3
Vulnerabilities:
  Gather data sampling:   Unknown: Dependent on hypervisor status
  Itlb multihit:          KVM: Mitigation: VMX unsupported
  L1tf:                   Mitigation; PTE Inversion
  Mds:                    Mitigation; Clear CPU buffers; SMT Host state unknown
  Meltdown:               Mitigation; PTI
  Mmio stale data:        Mitigation; Clear CPU buffers; SMT Host state unknown
  Reg file data sampling: Not affected
  Retbleed:               Mitigation; IBRS
  Spec rstack overflow:   Not affected
  Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl and seccomp
  Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
  Spectre v2:             Mitigation; IBRS; IBPB conditional; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI SW
                           loop, KVM SW loop
  Srbds:                  Not affected
  Tsx async abort:        Mitigation; Clear CPU buffers; SMT Host state unknow
```

memory stat

```
# free -h
               total        used        free      shared  buff/cache   available
Mem:            15Gi       1.8Gi        11Gi       1.8Gi       2.8Gi        11Gi
```
</details>


urls.txt
```
  urls.txt: |
    https://k8sblog.eumel.de
    https://github.com/eumel8/cosignwebhook/blob/main/README.md
    https://api.github.com/repos/eumel8/cosignwebhook
```

## Models

An LLM stands for Large Language Model, an AI system trained on vast text data to generate human-like text. The term "7b" refers to a 7 billion parameter model, often called a 7B model due to its size in billions (answer by Deepseek-R1)

### codellama:7b

A large language model that can use text prompts to generate and discuss code.

Company: Meta

Link: [https://ollama.com/library/codellama:7b](https://ollama.com/library/codellama:7b)

### deepseek-r1:7b

DeepSeek's first-generation of reasoning models with comparable performance to OpenAI-o1, including six dense models distilled from DeepSeek-R1 based on Llama and Qwen.

Company: Deepseek (CN)

Link: [https://ollama.com/library/deepseek-r1:7b](https://ollama.com/library/deepseek-r1:7b)

### dolphin3:latest

Dolphin 3.0 Llama 3.1 8B 🐬 is the next generation of the Dolphin series of instruct-tuned models designed to be the ultimate general purpose local model, enabling coding, math, agentic, function calling, and general use cases.

Link: [https://ollama.com/library/dolphin3:latest](https://ollama.com/library/dolphin3:latest)

### falcon3:latest

A family of efficient AI models under 10B parameters performant in science, math, and coding through innovative training techniques.

Link: [https://ollama.com/library/falcon3:latest](https://ollama.com/library/falcon3:latest)

### gemma:2b

Gemma is a family of lightweight, state-of-the-art open models built by Google DeepMind. Updated to version 1.1

hint: model 7b won't start due the system memory

Company: Gemini Deepmind (Google)

Link: [https://ollama.com/library/gemma:7b](https://ollama.com/library/gemma1:7b)


### llama3.1:8b

Llama 3.1 is a new state-of-the-art model from Meta available in 8B, 70B and 405B parameter sizes.

Company: Meta

Link: [https://ollama.com/library/llama3.1:8b](https://ollama.com/library/llama3.1:8b)

### mistral:7b

The 7B model released by Mistral AI, updated to version 0.3.

Company: Mistral AI (France)

Link: [https://ollama.com/library/mistral:7b](https://ollama.com/library/mistral:7b)

### qwen:7b

Company: Alibaba Cloud

Link: [https://ollama.com/library/qwen:7b](https://ollama.com/library/qwen:7b)

### tulu3:latest

Tülu 3 is a leading instruction following model family, offering fully open-source data, code, and recipes by the The Allen Institute for AI.

Company: Allen AI (Seattle, US)

Link: [https://ollama.com/library/tulu3:latest](https://ollama.com/library/tulu3:latest)
