

# 基于Dify的智能体/工作流开发实战


## Dify简介

Dify 是一个开源的 LLM 应用开发平台，核心目标是把大模型、提示词、知识库、工具调用和工作流编排整合到一个可视化平台中，让开发者可以更快地构建可发布、可调试、可运维的 AI 应用。

在 Dify 中，常见应用形态包括：

- **Chatbot**：面向普通对话问答，适合客服、知识助手、FAQ 等场景。
- **Agent**：让模型根据用户目标自主选择工具，例如搜索 GitHub、查询股票、调用地图服务。
- **Workflow**：把任务拆成稳定的节点流程，适合文档转换、内容生成、数据分析、图表生成等确定性更强的业务。
- **Chatflow**：面向多轮对话的工作流，兼顾 Workflow 的节点编排能力和 Chatbot 的对话体验。

本实训重点关注两类能力：一是用 **Agent** 接入工具完成开放式任务，二是用 **Workflow / Chatflow** 把复杂任务拆成可控流程。前置条件是先配置可用的大模型供应商，再按需配置插件、知识库或 MCP 工具。




## 访问方式

### 官网云服务

任何人都可以 开箱即用 Dify 的云服务。

地址： https://cloud.dify.ai/signin

可以直接使用邮箱登录

![image-20251024083852775](../../assets/dify001.png)



### ZTE iLab实训环境登录

课堂环境地址、账号和密码请以实训平台或教师现场发放的信息为准。公开文档中不放置真实服务器地址和登录凭据。

| 环境 | 内网地址 | 外网地址 | 用户名 | 密码 |
| --- | --- | --- | --- | --- |
| Dify 实训环境 1 | `http://<INTERNAL_DIFY_HOST_1>:<PORT>/apps` | `http://<PUBLIC_DIFY_HOST_1>:<PORT>/apps` | `<USERNAME>` | `<PASSWORD>` |
| Dify 实训环境 2 | `http://<INTERNAL_DIFY_HOST_2>:<PORT>/apps` | `http://<PUBLIC_DIFY_HOST_2>:<PORT>/apps` | `<USERNAME>` | `<PASSWORD>` |

### 本地化部署（可选，课后强化练习）

如果已经使用 Dify 云服务或 ZTE iLab 实训环境，可以跳过本节，直接进入“配置模型供应商”。本节只解决本地运行 Dify 的环境准备问题，后续 Agent / Workflow 开发流程与部署方式无关。

#### 安装说明

**系统资源要求：**

在开始安装 Dify 之前，请确保您的服务器或本地环境满足以下最低配置：

- **CPU：** 双核及以上
- **内存：** 至少 4 GiB

**推荐运行平台：**

- **Linux：** Ubuntu（推荐版本 22.04 或更高）
- **Windows：** 使用 **WSL2** 虚拟运行 Ubuntu 22.04，更多wsl的说明可以参考微软官网 [官网链接](https://learn.microsoft.com/en-us/windows/wsl/)



绝大情况下大家可能没有个人的服务器或者Linux系统，以下提供在window上WSL2 虚拟运行 Ubuntu 22.04的一页纸方法：

<details>
<summary>Windows / WSL2 / Docker 环境准备（可选，已有 Linux 或 Docker 环境可跳过）</summary>

##### wsl一页纸安装

网络状况好的情况下

```
# 一键安装 WSL2
wsl --install

```

网络状况不好

```
# 离线下载安装
地址： https://bgithub.xyz/microsoft/WSL/releases
安装包： wsl.2.6.1.0.x64.msi
通过浏览器下载会很慢，可以在目标链接上右键，选择“复制链接地址”，使用迅雷等第三方软件进行下载。

双击安装即可
```



##### wsl-ubuntu一页纸安装

```
# 安装 Ubuntu 22.04
wsl --install -d Ubuntu-22.04

# 查看发行版
wsl -l -v

# WSL2 的虚拟硬盘文件（`.vhdx`）默认占用系统盘空间，可能导致 C 盘空间不足。以下介绍如何查看默认存储位置并迁移到其他磁盘。建议必须操作
# 导出 Ubuntu 发行版 Ubuntu-22.04 到指定文件夹
wsl --export Ubuntu-22.04 D:\WSL\Ubuntu2204_backup.tar

# 注销旧发行版
wsl --unregister Ubuntu-22.04

# 导入到新位置：
wsl --import Ubuntu-22.04 D:\WSL\Ubuntu2204 D:\WSL\Ubuntu2204_backup.tar --version 2

# 验证迁移
wsl -l -v

# 性能增强
WSL2 的性能可以通过全局配置文件 .wslconfig 进行优化，文件位于：C:\Users\<用户名>\.wslconfig若文件不存在，需手动创建。
配置完需要重启： wsl --shutdown 在启动wsl

推荐配置模板
[wsl2]
memory=16GB              # 限制最大内存使用量
processors=4             # 指定 CPU 核心数
swap=8GB                 # 交换空间大小
swapFile=D:\WSL\swap.vhdx # 自定义 swap 文件路径
autoMemoryReclaim=true   # 自动回收未使用内存
localhostForwarding=true # 启用 localhost 端口转发
guiApplications=true     # 启用 WSLg（GUI 应用支持）
gpu=true                 # 启用 GPU 加速（需支持的 GPU 驱动）
dns=8.8.8.8              # 使用 Google DNS
networkingMode=mirrored  # 启用镜像网络模式（支持 IPv6）
firewall=true            # 启用 WSL 防火墙集成
autoProxy=true           # 自动使用 Windows 代理
nestedVirtualization=true # 启用嵌套虚拟化（适合运行 Docker 等）
```



如果中国区下载很慢

可以参考： https://blog.csdn.net/Mingcai_Xiong/article/details/147749696

```
打开浏览器访问以下网址：
👉 https://store.rg-adguard.net

在网页中：
第一个下拉框选择：ProductId
文本框输入：9PN20MSR04DW
第二个下拉框选择：Retail
点击 “✔ 生成链接”

下载文件
CanonicalGroupLimited.Ubuntu22.04LTS_2204.5.10021.0_neutral_~_79rhkp1fndgsc.AppxBundle
保存到本地电脑的 C:\wsl\

打开PowerShell，选择“以管理员身份运行”
运行安装命令
在 PowerShell 中，先切换到存放安装包的目录：
cd C:\wsl
然后，使用 Add-AppxPackage 命令来安装 Ubuntu：
Add-AppxPackage -Path .\CanonicalGroupLimited.Ubuntu22.04LTS_2204.5.10021.0_neutral_~_79rhkp1fndgsc.AppxBundle
```

> 如课堂提供离线安装包，请以课堂资料中的下载地址为准；公开文档中不放置临时网盘链接。



![image-20251029160212757](../../assets/image-20251029160212757.png)



更多可参考：[链接1](https://gitee.com/coderwillyan/learn-python-easily/blob/master/00_%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA/Windows-WSL-Ubuntu%E4%B8%8APython%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%85-Conda.md) ； [链接2](https://gitee.com/coderwillyan/learn-python-easily/blob/master/00_%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA/Windows-WSL-Ubuntu%E4%B8%8APython%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%85-Conda.md#wsl2-%E5%BF%AB%E9%80%9F%E5%8F%82%E8%80%83%E5%8D%A1%E7%89%87) ； 





##### docker一页纸安装

```markdown
# 安装必要的一些系统工具
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# 信任 Docker 的 GPG 公钥
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 写入软件源信息
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 配置镜像源
sudo mkdir -p /etc/docker  # 确保配置目录存在
sudo tee /etc/docker/daemon.json > /dev/null <<'EOF'
{
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF

# 重新启动docker
systemctl daemon-reload
systemctl restart docker

# 然后再pull所需镜像
```

</details>

##### dify一页纸安装

如需快速上手，请参考  👉 [Dify 自建部署（Docker Compose）](https://docs.dify.ai/getting-started/install-self-hosted)

> 若您希望更深入了解部署细节或自定义配置，可参考上方链接中的完整安装文档。

“一页式安装指南”：

```bash
(base) root@server5:/opt# git clone https://github.com/langgenius/dify.git
正克隆到 'dify'...
remote: Enumerating objects: 520525, done.
remote: Counting objects: 100% (23/23), done.
remote: Compressing objects: 100% (23/23), done.
remote: Total 520525 (delta 1), reused 2 (delta 0), pack-reused 520502 (from 2)
接收对象中: 100% (520525/520525), 452.44 MiB | 5.36 MiB/s, 完成.
处理 delta 中: 100% (382407/382407), 完成.
正在更新文件: 100% (13386/13386), 完成.

(base) root@server5:/opt# cd dify/docker/

(base) root@server5:/opt/dify/docker# cp .env.example .env

(base) root@server5:/opt/dify/docker# vim .env
修改内容： 默认插件下载速度会很慢，可以配置`.env`文件中的PIP镜像源：`PIP_MIRROR_URL`
PIP_MIRROR_URL=https://pypi.tuna.tsinghua.edu.cn/simple


(base) root@server5:/opt/dify/docker# docker compose -f docker-compose.yaml -p docker_dify up -d

[+] Running 86/86
 ✔ worker Pulled                                                                                                  56.0s
 ✔ plugin_daemon Pulled                                                                                           90.1s
 ✔ sandbox Pulled                                                                                                 50.5s
 ✔ ssrf_proxy Pulled                                                                                              47.1s
 ✔ db Pulled                                                                                                      31.7s
 ✔ worker_beat Pulled                                                                                             56.0s
 ✔ web Pulled                                                                                                     66.2s
 ✔ api Pulled                                                                                                     56.0s
 ✔ weaviate Pulled                                                                                                49.4s
 ✔ nginx Pulled                                                                                                   34.1s
 ✔ redis Pulled                                                                                                   20.8s
```

> 如果拉取较慢，可以选择逐个pull

```bash
(base) root@DESKTOP-WILL:/opt/dify/docker# docker compose pull nginx
```



至此就完成了在自己电脑上部署dify



#### 访问

访问地址：http://localhost:80

![image-20251024084626345](../../assets/dify002.png)





#### 主界面



![image-20251024084538751](../../assets/dify003.png)



#### 卸载
```
docker compose -f docker-compose.yaml -p docker_dify down
```

### 一台服务器部署多个Dify

如果防止端口冲突，不想使用默认的80和443端口

或者想在一台服务器部署多个dify
方法一：在运行 `docker compose` 启动服务是重新指定端口（推荐！）
第一个dify： 
```bash
cp -r docker docker_1280
```

```bash
EXPOSE_NGINX_PORT=1280 \
EXPOSE_NGINX_SSL_PORT=12443 \
EXPOSE_PLUGIN_DEBUGGING_PORT=15003 \
docker compose -f docker_1280/docker-compose.yaml -p docker_dify1280 up -d
```
第二个dify：
```bash
cp -r docker docker_2280
```

```bash
EXPOSE_NGINX_PORT=2280 \
EXPOSE_NGINX_SSL_PORT=22443 \
EXPOSE_PLUGIN_DEBUGGING_PORT=25003 \
docker compose -f docker_2280/docker-compose.yaml -p docker_dify2280 up -d
```

第三个dify：
```bash
cp -r docker docker_3280
```

```bash
EXPOSE_NGINX_PORT=3280 \
EXPOSE_NGINX_SSL_PORT=32443 \
EXPOSE_PLUGIN_DEBUGGING_PORT=35003 \
docker compose -f docker_3280/docker-compose.yaml -p docker_dify3280 up -d
```

第四个dify：
```bash
cp -r docker docker_4280
```

```bash
EXPOSE_NGINX_PORT=4280 \
EXPOSE_NGINX_SSL_PORT=42443 \
EXPOSE_PLUGIN_DEBUGGING_PORT=45003 \
docker compose -f docker_4280/docker-compose.yaml -p docker_dify4280 up -d
```

方法二：在运行 `docker compose` 启动服务之前先更新 **docker/.env** 文件内的变量。  
需要修改三个端口，修改.env文件，比如： 80 ->180  ； 443->1443  ； 5003->5103

```bash
# ------------------------------
# Docker Compose Service Expose Host Port Configurations
# ------------------------------
EXPOSE_NGINX_PORT=1280
EXPOSE_NGINX_SSL_PORT=12443

EXPOSE_PLUGIN_DEBUGGING_HOST=localhost
EXPOSE_PLUGIN_DEBUGGING_PORT=15003
```




## 配置模型供应商

在使用 Dify 构建Agent之前，需要先**选择并配置大模型供应商**，以便系统能够调用其提供的 API 接口。

由于 Agent 智能体的开发和运行会消耗较多的 Token（即调用费用 💰），建议优先选择**低成本或免费的模型服务**：

- **推荐选项 1：** 使用 **硅基流动（SiliconFlow）** 提供的 **免费 API**，可快速体验和测试。
- **推荐选项 2：** 使用 **中兴 iLab** 等 **本地部署的大模型**，既能节省成本，又能保障数据隐私与响应速度。

> ✅ 提示：在配置时，请根据所选供应商的文档，填写对应的 API Key、Base URL 等参数。

![image-20251027135707814](../../assets/image-20251027135707814.png)







### 硅基流动（SiliconFlow）配置指南

以 **硅基流动** 为例，它提供了多种免费模型资源，包括：

- **LLM 模型**（大语言模型）
- **Embedding 模型**（向量嵌入，用于语义检索等）
- **Rerank 模型**（重排序模型，用于结果优化）

------

#### 🧩 安装完成后

当您完成 Dify 的安装与启动后，可以在系统后台进入 **「模型供应商」** 页面进行配置。

![image-20251023091815918](../../assets/image-20251023091815918.png)

------

#### 🔑 获取 API Key

1. 登录硅基流动官网：
    👉 https://cloud.siliconflow.cn/me/account/ak
2. 进入「账户中心」→「API Key 管理」，创建并复制您的 **API Key**。

------

#### ⚙️ 在 Dify 中配置授权

在 Dify 控制台中：

1. 打开 **模型供应商配置** 页面；
2. 选择 **SiliconFlow**；
3. 在弹出的配置框中填写：
   - **API Base URL：** `https://api.siliconflow.cn/v1`
   - **API Key：** 粘贴上一步复制的密钥；
4. 点击 **保存配置**。

![image-20251023092047660](../../assets/image-20251023092047660.png)

------

#### 🧠 配置系统默认模型

完成供应商授权后，请在 Dify 的 **模型设置** 页面中，将硅基流动提供的模型设置为系统默认模型，例如：

- 默认 **对话模型（LLM）**
- 默认 **Embedding 模型**
- 默认 **Rerank 模型**

这样，Dify 在执行工作流或调用智能体时，将自动使用这些模型进行推理与处理。

![image-20251023092810939](../../assets/image-20251023092810939.png)

------

> 💡 提示：硅基流动的模型调用速度快、费用低，非常适合测试环境或中小规模的 Agent 开发场景。



### 本地部署 vLLM 配置指南

如果您选择在本地部署 **vLLM**，可以让 Dify 调用自建的大语言模型服务，避免公网调用带来的 **延迟、费用** 和 **隐私风险**。以下是配置步骤说明：

------

#### 🚀 部署 vLLM 服务

本次实践已在服务器上成功启动 vLLM，docker启动脚本如下：

```
(base) root@server5:/opt/workspace/Qwen_Start_via_Docker/startvllm# cat docker-compose-qwen3-14b.yml
# 启动
# docker compose -f docker-compose-qwen3-14b.yml up -d
#
# 查看日志
# docker-compose -f docker-compose-qwen3-14b.yml logs -f


version: '3.8'
services:
  qwen3-14b-server:
    image: vllm/vllm-openai:latest
    container_name: my-qwen3-14b-server
    runtime: nvidia  # 使用 NVIDIA 运行时
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              capabilities: [gpu]
              device_ids: ["0","1","2", "3"]  # 指定 GPU 2 和 3 [1,6](@ref)
    ports:
      - "9992:8000"  # 主机端口:容器端口，可按实际环境调整
    ipc: host  # 共享主机 IPC 命名空间
    volumes:
      - /opt/workspace/models/Qwen/Qwen3-14B:/models/Qwen3-14B  # 挂载模型目录
    command: [
      "--model", "/models/Qwen3-14B",
      "--max-model-len", "32768",
      "--tensor-parallel-size", "4",
      "--trust-remote-code",
      "--served-model-name", "my_qwen3_14b",
      "--dtype", "half",
      "--enable-auto-tool-choice",
      "--tool-call-parser", "hermes",
      "--reasoning-parser", "deepseek_r1",
      "--api-key", "YOUR_VLLM_API_KEY",
      "--gpu-memory-utilization", "0.8",
    ]

```

关键信息说明：

- `--served-model-name`：模型名称`my_qwen3_14b`
- `--port`：容器内默认 `8000`，主机端口按实际环境映射，例如 `9992`
- `--api-key`：密钥示例为 `YOUR_VLLM_API_KEY`，请替换为自己的值

启动后，您应能通过以下地址访问 OpenAI 兼容接口：

```
http://<YOUR_SERVER_IP>:9992/v1
```

------

#### 🔑 在 Dify 中添加模型供应商

1. 打开 Dify 控制台 → **设置 → 模型供应商**；

2. 选择 **vllm** ，添加模型；

   ![image-20251024085017173](../../assets/image-20251024085017173.png)

3. 在配置项中填写：

   | 参数                  | 输入值                                                       | 说明                        |
   | --------------------- | ------------------------------------------------------------ | --------------------------- |
   | **模型名称**          | `my_qwen3_14b`                                               |                             |
   | **模型类型**          | `LLM`                                                        |                             |
   | **API endpoint  URL** | 内网`http://<INTERNAL_SERVER_IP>:9992/v1`<br />外网`http://<PUBLIC_SERVER_IP>:9992/v1` | vLLM 服务地址               |
   | **API Key**           | `YOUR_VLLM_API_KEY`                                          | 与 vLLM 启动参数保持一致 |

   ![image-20251024085515135](../../assets/image-20251024085515135.png)





![image-20251024085445759](../../assets/image-20251024085445759.png)



![image-20251024085540615](../../assets/image-20251024085540615.png)



### Xinference

如果你想使用 **Xinference**（由 **Xorbits / InternLM 团队** 开发的本地多模型推理框架），它同样可以作为 **Dify 的模型供应商**，通过 **OpenAI 兼容 API 接口** 调用。下面是详细的配置说明 👇



#### 🚀 安装与启动 Xinference

![image-20251024101644525](../../assets/image-20251024101644525.png)

------



------

#### 🔑 在 Dify 中配置

1. 打开 Dify 控制台 → **设置 → 模型供应商**

2. 选择 **Xorbits Inference** 类型

3. 填写以下信息：

   | 参数          | 填入值                                                       | 说明                |
   | ------------- | ------------------------------------------------------------ | ------------------- |
   | **模型名称**  | 自定义                                                       |                     |
   | **模型类型**  | `LLM`                                                        |                     |
   | **服务器URL** | 内网`http://<INTERNAL_SERVER_IP>:<XINFERENCE_PORT>/v1`<br />外网`http://<PUBLIC_SERVER_IP>:<XINFERENCE_PORT>/v1` | Xinference 服务地址 |
   | **模型UID**   | `my_qwen3_0.6b_x`                                            | 与启动命令一致      |

4. 点击 **保存**，完成配置。

![image-20251024110058991](../../assets/image-20251024110058991.png)

### 模型供应商对比建议

| 方案                    | 优点                                   | 适用场景                     |
| ----------------------- | -------------------------------------- | ---------------------------- |
| **硅基流动**            | 云端免费、免运维、上手快               | 轻量测试、教学演示           |
| **vLLM 本地部署**       | 高性能推理、可定制模型、兼容OpenAI接口 | 企业内部部署、GPU服务器      |
| **Xinference 本地部署** | 支持多模型、管理便捷、易扩展           | 本地多模型管理、混合推理场景 |



![image-20251027142221192](../../assets/image-20251027142221192.png)



### 模型参数配置说明

#### 1️⃣ 温度（Temperature）

- **默认值：0.6**
- 控制模型输出的“随机性”。
  - 较低值（如 0.2） → 输出更稳定、更保守；
  - 较高值（如 0.8~1.0） → 输出更有创意，但也可能不太一致。
     📘 通常用于平衡“创造力 vs 准确性”。

------

#### 2️⃣ Top P（核采样，Nucleus Sampling）

- **默认值：0.95**
- 控制生成文本时，从概率最高的前 *P* 百分比的词中采样。
  - 例如 Top P=0.95 表示模型从累计概率为95%的词中挑选下一个词。
     📘 与温度一起使用时，可以显著影响生成的多样性。

------

#### 3️⃣ 最大标记数（Max Tokens）

- **默认值：8192**
- 限制模型生成的 **最大输出长度（token数）**。
  - 一个 token 大约相当于英文的 3~4 个字符，或中文的 1~2 个字。
     📘 如果生成太长内容，可调小；要生成文章或代码时，可调大。

------

#### 4️⃣ 思考模式（Think Mode）

- **选项：True / False**
- 当设为 `True` 时，模型在生成内容前会进入“思考阶段”，即内部进行隐式推理。
  - 在一些系统中，这对应 `<think>` 标签包裹的推理过程。
  - 设置为 `False` 则直接输出结果，不打印或执行显式推理。
     📘 常用于复杂逻辑推理、决策或规划任务。

------

#### 5️⃣ 思考长度限制（Think Length Limit）

- **默认值：512**
- 限制“思考模式”下模型内部推理内容的最大 token 数。
  - 值越大 → 模型思考更充分，但计算成本更高。
  - 值越小 → 思考速度快但可能不够深入。



![image-20251029110217658](../../assets/image-20251029110217658.png)

## Agent开发

### Agent开发五大核心要素

**内置 美股投资分析助手 样例** 

五个要素： 
- 提示词（Instructions）
- 变量（Variables）
- 知识库（Knowledge Base）
- 工具（Tools）
- 模型（Models）



![image-20251023095817623](../../assets/image-20251023095817623.png)





#### 🤖 核心要素一：提示词

提示词是Agent的“大脑”和“作战手册”，它定义了Agent的角色、目标、工作流程和行为准则。

- **角色与目标**：首先，你需要通过提示词为Agent设定一个明确的身份和要完成的核心任务。例如，“你是一名专业的旅行顾问，目标是为用户制定详尽的行程计划。”。
- **工作流程**：详细说明Agent接到任务后应该如何一步步执行，例如先理解问题，再调用哪个工具获取信息，最后如何组织回答。清晰的流程能显著提升Agent的推理和行动质量。
- **格式与风格**：可以规定输出格式（如使用Markdown、JSON）和语言风格（如专业严谨或轻松幽默），并可以加入限制条件，例如“避免讨论与主题无关的内容”。
- **设计技巧**：为了提高复杂任务（如分类）的准确性，可以在提示词中设计一个包含“类别定义”、“判断流程”和“输出格式”的精密结构，这相当于为模型构建了一个专家系统。

```
# 职位描述：数据分析助手
## 角色
我的主要目标是为用户提供专家级的数据分析建议。利用详尽的数据资源，告诉我您想要分析的股票（提供股票代码）。我将以专家的身份，为您的股票进行基础分析、技术分析、市场情绪分析以及宏观经济分析。

## 技能
### 技能1：使用Yahoo Finance的'Ticker'搜索股票信息
### 技能2：使用'News'搜索目标公司的最新新闻
### 技能3：使用'Analytics'搜索目标公司的财务数据和分析

## 工作流程
询问用户需要分析哪些股票，并按顺序执行以下分析：
**第一部分：基本面分析：财务报告分析
*目标1：对目标公司的财务状况进行深入分析。
*步骤：
1. 确定分析对象：
<记录 1.1：介绍{{company}}的基本信息>
2. 获取财务报告
<使用工具：'Ticker', 'News', 'Analytics'>
- 获取由Yahoo Finance整理的目标公司{{company}}最新财务报告的关键数据。
<记录 1.2：记录分析结果获取日期和来源链接>
5. 综合分析和结论：
- 全面评估公司的财务健康、盈利能力、偿债能力和运营效率。确定公司面临的主要财务风险和潜在机会。
-<记录 1.3：记录总体结论、风险和机会。>
整理并输出[记录 1.1] [记录 1.2] [记录 1.3] 
第二部分：基本面分析：行业
*目标2：分析目标公司{{company}}在行业中的地位和竞争力。
*步骤：
1. 确定行业分类：
- 搜索公司信息，确定其主要业务和行业。
-<记录 2.1：公司的行业分类>
2. 市场定位和细分分析：
- 了解公司在行业中的市场份额、增长率和竞争对手，进行分析。
-<记录 2.2：公司的市场份额排名、主要竞争对手、分析结果和洞察等。>
3. 行业分析
- 分析行业的发展趋势。
- <记录 2.3：行业的发展趋势。>
整理并输出[记录 2.1] [记录 2.2] [记录 2.3]
整合以上记录，并以投资分析报告的形式输出所有分析。使用Markdown语法进行结构化输出。

## 限制
- 使用的语言应与用户的语言相同。
- 避免回答有关工作工具和规章制度的问题。
- 使用项目符号和Markdown语法给出结构化回答，逐步思考。首先介绍情况，然后分析图表中的主要趋势。
```





#### ⚙️ 核心要素二：变量

变量为Agent应用提供了**动态化和可交互的能力**。它们作为占位符，允许用户在每次交互时输入不同的具体值，使同一个Agent能够处理大量个性化请求。

- **创建与使用**：在Dify的提示词或工作流中，使用`{{变量名}}`的格式来定义变量，例如`{{目的地}}`、`{{预算}}`。
- **用户界面**：当您发布应用后，这些变量会在前端呈现为输入框，用户无需修改提示词即可提交特定查询，极大地提升了用户体验的灵活性。
- **应用场景**：在旅行规划Agent中，变量可以是`目的地`、`旅行天数`和`预算`；在文本生成Agent中，变量可以是`场景`和`情绪`。

```
{{company}}
```

#### 📚 核心要素三：知识库

知识库通过**检索增强生成（RAG）** 技术为Agent注入**专业、实时的私有知识**，使其回答基于特定信息而非仅依赖模型的通用训练数据。

- **构建过程**：在Dify中，您可以上传文档（如PDF、Word）、输入文本或通过URL抓取网页内容来构建知识库。平台会自动对文档进行分片、向量化并存入向量数据库。
- **检索与集成**：当用户提问时，Agent会从知识库中检索最相关的信息片段，并将其作为上下文提供给大模型，从而生成具有针对性的精准答案。这对于构建企业级知识问答系统至关重要。
- **元数据过滤**：元数据过滤是使用元数据属性（例如标签、类别或访问权限）来细化和控制系统内相关信息的检索过程。
- **关键特性**：Dify和FastGPT等平台通常支持**混合检索**（结合向量检索和全文检索）和**引用溯源**，确保检索结果既准确又可验证。

![image-20251027144454986](../../assets/image-20251027144454986.png)



#### 🛠️ 核心要素四：工具

工具是Agent的“手脚”，**极大地扩展了模型的能力边界**，使其能够与现实世界进行交互，执行模型本身无法完成的具体操作。

- **工具类型**：**内置工具**：Dify平台提供了开箱即用的工具，如**网络搜索**（获取最新信息）、**计算器**、**知识库检索**等。**自定义工具**：您可以将任何符合OpenAPI规范的API接口（如查询数据库、发送邮件、调用内部系统）作为自定义工具接入Agent，实现强大的业务集成。
- **调用方式**：Agent根据提示词中的指令和用户需求，通过**Function Calling**或**ReAct**框架自动判断并调用合适的工具。

![image-20251027144734624](../../assets/image-20251027144734624.png)



#### ⚙️ 核心要素五：大模型

配置模型

![image-20251027144905973](../../assets/image-20251027144905973.png)



#### 💎 总结：如何协同工作

一个设计精良的Dify Agent，其工作流程通常是这四个要素的完美配合：

1. 用户通过**变量**提交具体请求。
2. **提示词**作为总指挥，根据请求规划行动步骤。
3. 如需外部知识，**提示词**会指示Agent调用**知识库**工具进行检索。
4. 如需执行具体操作（如计算、搜索、查询），**提示词**会指示Agent调用相应的**工具**。
5. 最终，模型将检索到的知识、工具返回的结果与用户请求相结合，生成最终回答。



### 聚焦点：提示词

风格一：

```markdown
<instruction>
请根据以下输入变量，分析该A股投资的相关信息，并提供详细的分析报告。分析内容应包括但不限于公司基本面、行业前景、财务状况、技术面分析、市场情绪以及投资建议。请确保分析报告内容准确、客观，不使用任何XML标签。

步骤：
1. 首先，分析公司的基本面，包括盈利能力、成长性、运营效率和财务健康度。
2. 其次，评估所处行业的整体发展趋势和竞争格局。
3. 然后，查看最近的财务数据，如收入、利润、资产负债率、现金流等。
4. 接着，进行技术面分析，包括股价走势、成交量、关键支撑和阻力位、技术指标（如均线、MACD、RSI）等。
5. 最后，根据以上分析给出综合的投资建议，说明买入、持有或卖出的理由，以及预期回报和风险提示。
</instruction>

<input>
{{stock_code}}：A股股票代码（如：600000）  
{{stock_name}}：A股股票名称（如：中国石油）  
</input>

<output>
完整的A股投资分析报告，包括基本面、行业、财务、技术面分析及投资建议。
</output>

<example>
输入示例：
stock_code：600519  
stock_name：贵州茅台  
industry：白酒  
recent_fiscal_data：2023年净利润为580亿，营收1100亿，资产负债率45%  
technical_analysis：股价持续上涨，突破年线，MACD柱状体持续放大，RSI在50以下，趋势偏多  

输出示例：
分析报告：贵州茅台（600519）作为白酒行业龙头，具备强大的品牌护城河和稳定的高端消费市场。根据2023年的财务数据，公司净利润达580亿，营收为1100亿，资产负债率45%，显示良好的财务健康度和低杠杆水平。技术面分析显示股价持续上涨，已突破年线，MACD柱状体持续放大，RSI处于50以下，走势强势，短期可能仍有上涨空间。综合来看，该股具有长期投资价值，建议投资者在当前价格区间逢低布局，同时注意市场波动风险。
</example>
```

风格二：

```markdown
# 职位描述：数据分析助手
## 角色
我的主要目标是为用户提供专家级的数据分析建议。利用详尽的数据资源，告诉我您想要分析的股票（提供股票代码）。我将以专家的身份，为您的股票进行基础分析、技术分析、市场情绪分析以及宏观经济分析。

## 技能
### 根据配置的工具进行分析

## 工作流程
询问用户需要分析哪些股票，并按顺序执行以下分析：
**第一部分：基本面分析：财务报告分析
*目标1：对目标公司的财务状况进行深入分析。
*步骤：
1. 确定分析对象：
<记录 1.1：介绍{{company}}的基本信息>
2. 获取财务报告
<使用工具>
- 获取由工具整理的目标公司{{company}}最新财务报告的关键数据。
<记录 1.2：记录分析结果获取日期和来源链接>
5. 综合分析和结论：
- 全面评估公司的财务健康、盈利能力、偿债能力和运营效率。确定公司面临的主要财务风险和潜在机会。
-<记录 1.3：记录总体结论、风险和机会。>
整理并输出[记录 1.1] [记录 1.2] [记录 1.3] 
第二部分：基本面分析：行业
*目标2：分析目标公司{{company}}在行业中的地位和竞争力。
*步骤：
1. 确定行业分类：
- 搜索公司信息，确定其主要业务和行业。
-<记录 2.1：公司的行业分类>
2. 市场定位和细分分析：
- 了解公司在行业中的市场份额、增长率和竞争对手，进行分析。
-<记录 2.2：公司的市场份额排名、主要竞争对手、分析结果和洞察等。>
3. 行业分析
- 分析行业的发展趋势。
- <记录 2.3：行业的发展趋势。>
整理并输出[记录 2.1] [记录 2.2] [记录 2.3]


整合以上记录，并以投资分析报告的形式输出所有分析。分析目标公司{{company}}股票当前是否推荐购买，给出结论。使用Markdown语法进行结构化输出。

## 限制
- 使用的语言应与用户的语言相同。
- 避免回答有关工作工具和规章制度的问题。
- 使用项目符号和Markdown语法给出结构化回答，逐步思考。首先介绍情况，然后分析图表中的主要趋势。
```

### 聚焦点：知识库

可以接入Dify平台搭建的知识库或者RAGFlow的知识库。
接入Dify平台搭建的知识库不多做赘述，推荐RAGFlow知识库接入，效果更好：  

在 Dify 中配置 RAGFlow 的知识库时，需要在 RAGFlow 的基础 Base url 后增加 “api/v1/dify”，这是 Dify 特定的 API 路径，它承担版本控制、模块划分等作用。当然这也很符合 RESTful 的设计思想。
创建知识库  

完成 Dify 和 RAGFlow 的 API 连接之后，就可以紧接着创建知识库，需要注意的是，需要点击的是“连接外部知识库”这个按钮。下一步会提示需要输入外部知识库 ID，这个信息需要在大家 RAGFlow 对应的知识库页面，在浏览器的地址后缀上能看到完整的 ID 数字，直接复制过来填下。  

连通测试  
在创建完知识库后，可以大家这个知识库进行召回测试，这个类似 RAGFlow 的检索测试功能，主要是为了检验下上述的两步配置是否成功。需要注意的是，在这一步还不需要配置 LLM 即可进行测试。  



### 聚焦点：工具管理

#### 常用工具

JINA AI：数据抓取， Jina AI 是一个开源神经搜索框架，用于构建可扩展的多模态 AI 应用程序。它提供了用于索引和检索各种数据的工具，包括细分网页、获取单个页面和搜索网站的能力。它专注于简化复杂的人工智能搜索功能，并使网络数据处理更容易。

#### 内置工具配置

在marketplace安装已上架的插件：http://<IP>/tools

![image-20251023095757438](../../assets/image-20251023095757438.png)



![image-20251023095936344](../../assets/image-20251023095936344.png)



部分插件需要配置API，以`GitHub`插件为例： 



![image-20251024094208941](../../assets/image-20251024094208941.png)



![image-20251024094220567](../../assets/image-20251024094220567.png)

跟据 `从GitHub 获取您的 Access Tokens` 指引进行获取

![](../../assets/image-20251024094426989.png)





![image-20251024094453056](../../assets/image-20251024094453056.png)

完成API Key授权配置

![image-20251024094543180](../../assets/image-20251024094543180.png)

配置完成

![image-20251024094650625](../../assets/image-20251024094650625.png)

工具可见

![image-20251024094718398](../../assets/image-20251024094718398.png)





#### MCP工具配置：MCP服务提供商ModelScope为例

如果内置工具没有呢？

你可以在 Dify 的 Agent 和 Workflow 应用中，直接集成来自外部 [MCP](https://modelcontextprotocol.io/introduction) 服务器的[工具](https://modelcontextprotocol.io/docs/concepts/tools)。除了使用 Dify 内置插件外，还可以接入 MCP [生态系统](https://mcpservers.org/)中的第三方服务，持续扩展你的应用功能。

登录 Dify 后，在左侧导航栏中依次点击 **工具** → **MCP**，即可进入外部 MCP 服务器的管理页面。在这里，你可以统一管理所有为自身应用配置的 MCP 服务器。

![image-20251023142636074](../../assets/image-20251023142636074.png)

##### 🪄 启用 ModelScope MCP 服务

1️⃣ **登录 ModelScope 官网**
 👉 https://modelscope.cn/mcp

2️⃣ **搜索目标服务**
 在搜索栏中输入 **“高德地图”**，找到对应的 **MCP 服务**。

> 💡 建议：Dify 使用 **SSE 模式** 通信更流畅、稳定，因此推荐选择 **SSE 模式** 的服务端点。

![image-20251027165234263](../../assets/image-20251027165234263.png)

------

##### 🔑 申请高德地图 API Key

1️⃣ **访问高德开放平台**
 👉 https://console.amap.com/dev/index

2️⃣ **创建应用并申请 API Key**
 申请字段：`AMAP_MAPS_API_KEY`

3️⃣ **填写到 ModelScope MCP 配置中**

例如：`YOUR_AMAP_MAPS_API_KEY`

4️⃣ **选择鉴权类型**：`Bearer Token`

5️⃣ **生成配置信息**
 系统会返回如下示例 JSON：

```
{
  "mcpServers": {
    "amap-maps": {
      "type": "sse",
      "url": "https://mcp.api-inference.modelscope.net/<YOUR_MODELSCOPE_MCP_ID>/sse",
      "headers": {
        "Authorization": "Bearer YOUR_MODELSCOPE_MCP_TOKEN"
      }
    }
  }
}
```

------

##### ⚙️ 在 Dify 中添加 MCP 服务器

1️⃣ **打开配置入口**
 Dify 控制台 → **设置 → MCP 服务提供商 → 添加 MCP 服务器**

2️⃣ **填写配置信息：**

| 🔧 配置项         | 🧾 示例值                                                     | 💬 说明                      |
| ---------------- | ------------------------------------------------------------ | --------------------------- |
| **服务端点 URL** | `https://mcp.api-inference.modelscope.net/<YOUR_MODELSCOPE_MCP_ID>/sse` | ModelScope MCP SSE 通信地址 |
| **请求头名称**   | `Authorization`                                              | 固定字段                    |
| **请求头值**     | `Bearer YOUR_MODELSCOPE_MCP_TOKEN`                          | ModelScope 生成的 Token     |

3️⃣ **点击「保存」** 完成配置。

![image-20251027163708210](../../assets/image-20251027163708210.png)

------

##### ✅ 查看授权结果

- 若连接成功，Dify 会显示 **“已连接”** 状态；
- 之后即可在 **工作流节点** 或 **智能体工具** 中直接调用 **高德地图服务**。

![image-20251027163809205](../../assets/image-20251027163809205.png)



##### 💎 其他MCP服务提供商

**阿里百炼：**

官网：https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.11cf7980vWPIhp&tab=mcp#/mcp-market

| 🔧 配置项         | 🧾 示例值                                                   | 💬 说明                    |
| ---------------- | ---------------------------------------------------------- | ------------------------- |
| **服务端点 URL** | `https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse` | aliyuncs MCP SSE 通信地址 |
| **请求头名称**   | `Authorization`                                            | 固定字段                  |
| **请求头值**     | `Bearer YOUR_DASHSCOPE_API_KEY`                            | aliyuncs 生成的 Token     |

**composio：**

官网：https://mcp.composio.dev/dashboard/apps




#### MCP工具配置：工具->MCP SSE / StreamableHTTP

通过 HTTP with SSE 或 Streamable HTTP 传输方式使用 MCP 协议来发现和调用工具。



**安装插件**

在 Agent 中调用 MCP 首先得安装个【MCP SSE】的插件。

点击右上角插件，选择从 Marketplace 中安装，搜索 mcp，找到【MCP_SSE】，点击安装。





## 工作流



工作流通过将复杂的任务分解成较小的步骤（节点）降低系统复杂度，减少了对提示词技术和模型推理能力的依赖，提高了 LLM 应用面向复杂任务的性能，提升了系统的可解释性、稳定性和容错性。Dify 工作流分为两种类型：

- **Chatflow**：面向对话类情景，包括客户服务、语义搜索、以及其他需要在构建响应时进行多步逻辑的对话式应用程序。
- **Workflow**：面向自动化和批处理情景，适合高质量翻译、数据分析、内容生成、电子邮件自动化等应用程序。

为解决自然语言输入中用户意图识别的复杂性，Chatflow 提供了问题理解类节点。相对于 Workflow 增加了 Chatbot 特性的支持，如：对话历史（Memory）、标注回复、Answer 节点等。

为解决自动化和批处理情景中复杂业务逻辑，工作流提供了丰富的逻辑节点，如代码节点、IF/ELSE 节点、模板转换、迭代节点等，除此之外也将提供定时和事件触发的能力，方便构建自动化流程。

节点说明参考：https://docs.dify.ai/zh-hans/guides/workflow/node/start



### 智能体与工作流对比

在 Dify 中，Agent 和 Workflow 都可以调用大模型、工具和知识库，但设计思路不同：

| 维度 | Agent 智能体 | Workflow 工作流 |
| --- | --- | --- |
| 核心思路 | 让模型根据目标自主规划、选择工具、组织答案 | 开发者预先设计节点流程，按固定链路执行 |
| 适合任务 | 开放式、探索式、步骤不固定的任务 | 流程清晰、步骤稳定、需要可控输出的任务 |
| 工具调用 | 由模型判断是否调用、调用哪个工具 | 由流程节点明确指定调用哪个工具 |
| 稳定性 | 更灵活，但结果受模型推理和提示词影响更大 | 更稳定，节点和分支清晰，便于调试 |
| 可解释性 | 需要查看模型思考和工具调用记录 | 每个节点输入输出明确，更容易定位问题 |
| 维护方式 | 重点维护提示词、工具说明和约束条件 | 重点维护节点编排、变量传递和异常分支 |
| 典型案例 | GitHub 项目发现、投资分析助手、路线规划助手 | Markdown 转 DOCX、SEO 文章生成、数据可视化报表 |

简单判断：

- 如果任务像“帮我调研一下”“帮我分析一下”“自己决定查什么资料”，优先考虑 **Agent**。
- 如果任务像“先做 A，再做 B，最后输出 C”“每一步都希望稳定可控”，优先考虑 **Workflow**。
- 如果既要多轮对话，又要节点编排和状态管理，优先考虑 **Chatflow**。
- 在生产场景中，常见做法是先用 Agent 快速验证想法，再把稳定下来的步骤沉淀成 Workflow。

## 导入 yml 示例并验证

本目录提供了一组 Dify DSL 示例文件，路径为 `3.4大模型-Agent/04_Dify/yml/`。Dify DSL 是 Dify 应用的 YAML 导入/导出格式，官方说明可参考：https://docs.dify.ai/en/use-dify/workspace/app-management

### 导入步骤

1. 进入 Dify 控制台，打开 **工作室 / Studio**。
2. 点击 **创建应用**，选择 **导入 DSL 文件** 或 **从 DSL 文件导入**。
3. 上传本目录中的 `.yml` 文件。
4. 导入后先打开应用配置页，检查模型供应商、工具插件、MCP 服务是否已安装并授权。
5. 点击 **调试 / Preview** 运行一次，确认节点、工具和模型都能正常返回结果。
6. 验证通过后再点击 **发布 / Publish**，生成 Web App、API 或嵌入式 Chatbot。

### 示例清单

| 文件 | 类型 | 依赖重点 | 建议验证方式 |
| --- | --- | --- | --- |
| `A股投资分析助手-Agent.yml` | Agent | Investoday 股票工具、时间工具、可用 LLM | 输入股票代码或公司名，检查是否能生成结构化投资分析报告 |
| `GitHub优秀项目发现DevSpotter-Agent.yml` | Agent | GitHub 插件及 GitHub Token | 输入主题，如 `RAG framework`，检查是否能搜索仓库并总结价值 |
| `智能路线规划助手-Agent.yml` | Agent | ModelScope / 高德地图 MCP 工具 | 输入起点、终点、交通方式，检查是否能调用地图工具 |
| `智能路线规划助手-工作流.yml` | Workflow | ModelScope / 高德地图 MCP 工具 | 在开始节点填写起点、终点、偏好，检查路线报告输出 |
| `markdown转docx文件工作流.yml` | Workflow | Markdown 转 DOCX 插件 | 上传 Markdown 文件，检查是否生成可下载的 DOCX |
| `echart数据可视化助手.yml` | Workflow | 文件上传、代码/图表生成节点 | 上传示例 Markdown 数据，检查是否生成图表配置或图表结果 |
| `echart数据可视化助手2.0.yml` | Workflow | ECharts 插件 | 上传 `echart数据可视化助手demo数据.md` 或表格数据，检查柱状图输出 |
| `SEO 博客生成工作流.yml` | Workflow | 可用 LLM、搜索工具/MCP | 输入关键词、标题、受众和语气，检查是否生成完整 SEO 文章 |

### 导入后的常见检查项

- **模型不可用**：进入 **设置 → 模型供应商**，重新选择当前环境已有的 LLM、Embedding 或 Rerank 模型。
- **插件缺失**：进入 **工具 / Marketplace** 安装缺失插件，例如 GitHub、ECharts、Markdown Exporter。
- **MCP 未连接**：进入 **工具 → MCP**，把文档中的 `YOUR_*` 占位符替换为自己的服务端点和 Token。
- **变量缺失**：检查开始节点或 Agent 变量表，确认必填字段已经填写。
- **输出为空**：先单独调试失败节点，再运行完整流程；优先检查工具授权、模型上下文长度和输入文件格式。

# 练习主题 

**可选主题：**（最终Agent名字大家可以自己取）

1. 优秀开源项目智能发现与评估专家（github等工具）
2. 12306车票查询专家（12306）
3. 论文检索专家（Arxiv等等）
4. 智能线路规划专家（高德地图）
5. 多平台视频内容检索专家（bilibili）
6. A股股票投资分析专家（今日投资数据）
7. 菜谱推荐专家（今天吃什么）



**选择用以下三种方式搭建：**

- Agent
- Workflow
- Chatflow

**可以选择**

- 将结果保存到本地文件，markdown转换器，各种格式
- 将结果渲染成图表
- 这些参考的同级目录 `yml` 文件夹中工作流示例： 
  - markdown转docx文件工作流.yml
  - echart数据可视化助手2.0.yml

**可以选择**

- 发布，比如浏览器的Dify Chatbot 插件



