# ICOM 6045 通信网络安全 · L4a 中文预习版

## 缺失与待确认

已根据上传的 PPT 全文与图示整理，共 16 页。下列内容原讲义没有写清，预习时不要自行脑补成定论：

- 未另行指定读者程度与考试范围。本资料按大学课程预习处理。
- 第 2 页目录有 “Communication Security Issues（通信安全问题）”，后面没有以此为标题的独立页。相关内容落在第 12–16 页。
- 第 11 页没有标题、没有正文、也没有印页码，只有四张转发过程图。
- 第 9 页正文很短；应用层协议名单在第 10 页的协议图里。
- 没有演讲者备注。图中看不清的下标、图号，文中标为 `[待确认]`。
- 第 13 页与第 14 页使用同一张 “OSI 层 / 互联网层 / 安全机制” 对照图（文件大小不同，内容一致），讲的层次不同。

## 1. 封面信息

- 课程/主题：ICOM 6045 Communication Network Security（通信网络安全），第 L4a 讲；讲授人 K.P. Chow，香港大学（University of Hong Kong）
- 原始 PPT 页数：16 页（按放映顺序；第 1、11 页版面上未印页码，其余印出的页码与放映顺序一致）
- 预习版说明：本资料为中文翻译与预习重构，页码对应原 PPT
- 目标读者：大学生（课程代码为 ICOM 6045，程度未另行说明）
- 预计预习时间：约 40–50 分钟（精读约 35 分钟，自测约 10 分钟）

## 2. 学习目标

预习结束后，应当能够：

- [ ] 能够说明通信网络同时包含物理基础设施和逻辑基础设施（协议）
- [ ] 能够按顺序写出 TCP/IP 四层，并说出每层与 OSI 模型的大致对应关系
- [ ] 能够用封装过程说明：报文下到链路时加上哪些首部，交换机和路由器各处理到哪一层
- [ ] 能够比较链路层、互联网层、传输层、应用层安全的保护范围、优点和代价
- [ ] 能够区分 IPsec VPN 与 SSL/SSH 一类传输层方案：谁对应用透明，谁要求端口绑定
- [ ] 能够举出各层的安全例子：链路加密、IPsec（AH/ESP）、SSL/TLS 与 SSH、网银登录

## 3. 预习导航

- [1. 封面信息](#1-封面信息)
- [2. 学习目标](#2-学习目标)
- [3. 预习导航](#3-预习导航)
- [4. 核心概念速览](#4-核心概念速览)
- [5. 逐页精读](#5-逐页精读)
- [6. 术语表](#6-术语表)
- [7. 重点、难点与易错点](#7-重点难点与易错点)
- [8. 课前预习问题](#8-课前预习问题)
- [9. 自测题](#9-自测题)
- [10. 一页总结](#10-一页总结)

## 4. 核心概念速览

| 概念 | 中文解释 | 重要性 | 首次出现页码 |
| --- | --- | --- | --- |
| 通信网络 | 以电子形式交换信息的基础设施，分物理部分和逻辑部分 | 基础 | 第 3 页 |
| TCP/IP 模型 | 本讲的互联网四层模型：网络接入、互联网、传输、应用 | 高 | 第 5 页 |
| 网络接入层 | 大致对应 OSI 物理层 + 数据链路层，含 LLC 与 MAC | 高 | 第 6 页 |
| 互联网层 | 负责跨网络选路；IPv4 用 4 字节 IP 地址 | 高 | 第 7 页 |
| 传输层 | 在不同主机的进程之间交换数据，可可靠或不可靠 | 高 | 第 8 页 |
| 应用层 | 面向具体应用；对应 OSI 第 5–7 层 | 中 | 第 9 页 |
| 封装与逐跳转发 | 源主机逐层加首部；交换机只看链路层，路由器看到网络层 | 高 | 第 11 页 |
| 链路级加密 | 每一段链路两端加密；中间节点必须解密再加密 | 高 | 第 12 页 |
| IPsec | 互联网层安全，常见形式是 VPN；机制包括 AH 与 ESP | 高 | 第 13 页 |
| 传输层安全 | 如 SSL/TLS、SSH；应用往往要主动调用安全功能 | 高 | 第 14 页 |
| 端口绑定 | SSH 方案要求按邮件端口正确绑定；IPsec 方案不要求 | 高 | 第 15 页 |
| 应用层安全 | 只安装安全应用，不改操作系统；例子是网银登录 | 高 | 第 16 页 |

## 5. 逐页精读

### 第 1 页：课程封面

- **原文标题/关键词**：ICOM 6045 / Communication Network Security；K.P. Chow；University of Hong Kong
- **一句话总结**：本讲属于香港大学 ICOM 6045《通信网络安全》。
- **中文翻译/要点**：
  - 课程代码：ICOM 6045
  - 课程名称：通信网络安全（Communication Network Security）
  - 讲授人：K.P. Chow
  - 学校：香港大学（University of Hong Kong）
- **图表/图片说明**：无
- **预习疑问**：这一讲的 “网络” 是指哪一种网络，后面会不会只讲互联网？

### 第 2 页：本讲目录

- **原文标题/关键词**：Communication Network Security；Introduction；The Internet Model (TCP/IP Model)；Security at Different Layers；Communication Security Issues
- **一句话总结**：全讲先定义通信网络，再讲 TCP/IP 四层，最后按层讨论安全。
- **中文翻译/要点**：
  - 引言（Introduction）
  - 互联网模型，即 TCP/IP 模型（The Internet Model / TCP/IP Model）
  - 不同层次上的安全（Security at Different Layers）
  - 通信安全问题（Communication Security Issues）：目录中有这一项，后续没有同名标题页，内容体现在第 12–16 页
- **图表/图片说明**：无
- **预习疑问**：为什么讲安全之前，要先把 TCP/IP 四层讲清楚？

### 第 3 页：什么是通信网络

- **原文标题/关键词**：Introduction；communication network；physical infrastructure；logical infrastructure；communication protocols
- **一句话总结**：通信网络 = 可传信号的物理设施 + 给这些信号赋予含义的协议。
- **中文翻译/要点**：
  - 通信网络（communication network）：以电子形式交换信息的基础设施
  - 物理基础设施：通信链路（导线和电缆）、路由器（router）、中继器（repeater）以及其他设备
  - 逻辑基础设施：通信协议（communication protocol）。协议使线路上的电脉冲或二进制信息 “有意义”
- **图表/图片说明**：无
- **预习疑问**：如果两台设备物理上连得通，但协议不一致，信息交换会失败在哪一部分？

### 第 4 页：通信网络的类型

- **原文标题/关键词**：Communication Network；voice, documents, photos, or video；PSTN；mobile telephone network；the Internet；common infrastructure
- **一句话总结**：语音、文档、照片、视频可以走同一套通信网络，而不必各用一张专用网。
- **中文翻译/要点**：
  - 信息类型：语音、文档、照片或视频
  - 网络类型举例：
    - 公共交换电话网（public switched telephone network，常称 PSTN）
    - 移动电话网（mobile telephone network）
    - 互联网（the Internet）
  - 趋势：用一套公共基础设施（common infrastructure），也就是同一张通信网络，交换多种信息
- **图表/图片说明**：无
- **预习疑问**：电话网和互联网如果共用基础设施，安全边界还会不会按 “这是电话、那是上网” 分开？

### 第 5 页：TCP/IP 模型总览

- **原文标题/关键词**：The Internet Model (TCP/IP Model)；protocol suite；internetworking technology
- **一句话总结**：本讲所说的互联网，是指采用 TCP/IP 协议族做网络互连的网络。
- **中文翻译/要点**：
  - 互联网模型以 TCP/IP 协议族为基础
  - 协议族（protocol suite）：一组相互配合的通信协议
  - “Internet” 在这里指：使用这套协议族所实现的网络互连技术（internetworking）的网络
  - 图中四层自下而上为：
    1. 主机到网络（Host to network）
    2. 互联网（Internet）
    3. 传输（Transport）
    4. 应用（Application）
  - 最底层在后文还有另外两个名字：网络接入层（Network Access）、网络接口层（Network Interface）。本讲把它们看成同一层
- **图表/图片说明**：一张四层堆叠图，标题为 “TCP/IP Model”。自上而下是 Application、Transport、Internet、Host to network。没有标出具体协议。
- **难点标记**：⭐⭐ 重点
- **预习疑问**：协议族和单个协议（例如只说 IP 或只说 TCP）差在哪里？

### 第 6 页：网络接入层

- **原文标题/关键词**：Network Access Layer；OSI data link and physical layer；LLC；IEEE 802.2；MAC；Ethernet；IEEE 802.3；token ring；IEEE 802.5
- **一句话总结**：网络接入层让主机真正用上传输介质，并分成 LLC 和 MAC 两个子层。
- **中文翻译/要点**：
  - 网络接入层大致对应 OSI 的数据链路层和物理层
  - 作用：使主机与传输介质之间能够通信
  - 逻辑链路控制（Logical Link Control，LLC）子层，标准为 IEEE 802.2：
    - 在传输介质上为主机编址
    - 控制数据链路
    - 原文还写：在同一局域网（local area network，LAN）内的主机之间路由数据
  - 介质访问控制（Medium Access Control，MAC）子层把下面三件事 “隐藏” 起来：
    - 物理介质的具体种类，例如光纤或双绞线
    - 网络拓扑
    - 介质控制方式，例如基于 IEEE 802.3 的以太网（Ethernet），或 IEEE 802.5 的令牌环（token ring）
- **图表/图片说明**：无
- **难点标记**：⭐ 易错
- **预习疑问**：同一局域网里 “把帧送到另一台主机”，按原文算 LLC 的工作。你是否同意，还是更常把它归到 MAC/交换机？

> 原文把同一 LAN 内主机间的路由写在 LLC 上。多数教材把按 MAC 地址转发归到 MAC 子层和交换机。这里先按幻灯片记，并标 `[待确认]`：课堂是否会改口到 MAC。

### 第 7 页：互联网层与 IPv4 地址

- **原文标题/关键词**：Internet Layer；internetworking；routing；4-byte IP addresses (IPv4)；227.82.157.177
- **一句话总结**：互联网层用 IP 地址选路，使不在同一个局域网里的两台主机也能通信。
- **中文翻译/要点**：
  - 互联网层是互联网的核心，解决网络互连（internetworking）
  - 两台主机即使不接在同一个 LAN 上，也可以互发数据
  - 最重要的任务是路由（routing）：决定下一台该把数据交给谁。做决定的主机不必知道到目的地的整条实际路径
  - 路由依据是 4 字节的 IP 地址，即 IPv4
  - 图中的例子：
    - 点分十进制：`227.82.157.177`
    - 按 8 位一段写成二进制：`11100011 01010010 10011101 10110001`
    - 图注写的是：分成 8 位网络号（Network ID）和 24 位主机号（Host ID）。图上第一段与后三段颜色不同
- **图表/图片说明**：一张 IPv4 地址拆分图。上方刻度 0、8、16、24、32。第一行是二进制四段，第二行是点分十进制 227、82、157、177。底部两行文字为 “IP Address: 227.82.157.177” 和 “Split Into 8-Bit Network ID and 24-Bit Host ID”。

\[
227.82.157.177
= \underbrace{11100011}_{227}\;
\underbrace{01010010}_{82}\;
\underbrace{10011101}_{157}\;
\underbrace{10110001}_{177}
\]

- **难点标记**：⭐⭐ 重点
- **预习疑问**：路由器在 “不知道整条路径” 的情况下，仍然能转发，它至少要知道什么？

> `[待确认]`：`227.82.157.177` 的第一段是 `11100011`。按传统分类编址，`1110` 开头属于 D 类（224–239），并不是 “8 位网络号 + 24 位主机号” 的 A 类地址。图注仍这样划分。预习时把它当成 “幻灯片上的拆法”，不要当成分类编址的标准例题。

### 第 8 页：传输层

- **原文标题/关键词**：Transport Layer；host-host layer；processes；logical connections；reliably or unreliably；TCP；UDP
- **一句话总结**：传输层在不同主机上的进程之间建立逻辑连接，并决定可靠还是不可靠地送数据。
- **中文翻译/要点**：
  - 传输层又称主机到主机层（host-host layer）
  - 支持运行在不同主机上的进程交换数据
  - 负责建立设备之间的逻辑连接，使数据可以不可靠地发送，也可以可靠地发送
  - 本页点名的两个协议：
    - 传输控制协议（Transmission Control Protocol，TCP）
    - 用户数据报协议（User Datagram Protocol，UDP）
- **图表/图片说明**：无
- **难点标记**：⭐ 易错
- **预习疑问**：互联网层已经能把 IP 包送到另一台主机，为什么还需要传输层？

> 幻灯片只并列写出 “可靠或不可靠”，并列出 TCP 与 UDP，没有逐条对照。课堂通常把 TCP 对应可靠、UDP 对应不可靠，但这句对应关系不是本页原文，标 `[待确认]`。

### 第 9 页：应用层

- **原文标题/关键词**：Application Layer；process/application layer；OSI model layers five through seven
- **一句话总结**：TCP/IP 的应用层是 “进程/应用层”，一把拿走 OSI 的第 5、6、7 层。
- **中文翻译/要点**：
  - 这一层也叫进程/应用层（process/application layer）
  - 它覆盖 OSI 模型的第 5 层到第 7 层（会话层、表示层、应用层）
  - 本页没有展开具体协议；协议名单见第 10 页
- **图表/图片说明**：无
- **预习疑问**：OSI 有七层，TCP/IP 只有四层。少掉的三层功能是消失了，还是被并进应用层？

### 第 10 页：TCP/IP 协议图

- **原文标题/关键词**：TCP/IP Protocols；DNS；TCP；UDP；IP；IPsec；ARP；PPP
- **一句话总结**：一张总图把常见协议按层放好；安全课后面会反复用到其中的 IPsec、TCP/UDP 和应用协议。
- **中文翻译/要点**：
  - 这张图用 OSI 式层号（2–7）标注，但讲义自身的模型仍是四层。阅读时以四层为准，层号只是图上的坐标
  - **应用层（图上第 5–7 层）**

    | 功能分组 | 图中协议 |
    | --- | --- |
    | 名字系统（Name System） | DNS |
    | 文件共享（File Sharing） | NFS |
    | 主机配置（Host Config） | BOOTP、DHCP |
    | 网络管理（Network Mgmt） | SNMP、RMON |
    | 文件传输（File Transfer） | FTP、TFTP |
    | 电子邮件与新闻（E-Mail & News） | RFC 822/MIME、SMTP、POP/IMAP、NNTP |
    | Web 与 Gopher | HTTP、Gopher |
    | 交互式（Interactive） | Telnet、r 命令（r-commands）、IRC |

  - **传输层（图上第 4 层）**：UDP、TCP
  - **互联网层（图上第 3 层）**：
    - IP NAT
    - 网际协议 IP（IPv4、IPv6）
    - IPsec
    - 移动 IP（Mobile IP）
    - IP 支撑协议：ICMP/ICMPv4、ICMPv6、邻居发现（Neighbor Discovery，ND）
    - IP 路由协议：RIP、OSPF、GGP、HELLO、IGRP、EIGRP、BGP、EGP
  - **画在互联网层与网络接口层之间**：地址解析协议（Address Resolution Protocol，ARP）、反向地址解析协议（Reverse Address Resolution Protocol，RARP）
  - **网络接口层（图上第 2 层）**：串行线路接口协议（Serial Line Interface Protocol，SLIP）、点到点协议（Point-to-Point Protocol，PPP）、局域网/无线局域网/广域网硬件驱动（LAN/WLAN/WAN Hardware Drivers）
- **图表/图片说明**：整页是一张协议地图，标题 “TCP/IP Protocols” 放在页面一侧。图中带有水印式底纹。ARP 与 RARP 单独占互联网层和网络接口层之间的位置。路由协议清单里有一些早期协议（如 GGP、HELLO、EGP），图上只列名称，没有解释现状。
- **难点标记**：⭐⭐ 重点
- **预习疑问**：如果安全做在 IP 这一层，图上哪些协议的流量可以一起被保护，而不必逐个应用去改？

### 第 11 页：从源主机到目的主机的四步转发

- **原文标题/关键词**：无标题页。图中文字：Source；Destination；Link-layer Switch；Router；Application / Transport / Network / Link / Physical；\(M\)、\(H_t\)、\(H_n\)、\(H_1\)；Delivery from Source to Switch / Switch to Router / Router to Switch / Switch to Destination
- **一句话总结**：数据每向下一层就加一个首部；交换机只处理到链路层，路由器处理到网络层，目的主机再逐层拆开。
- **中文翻译/要点**：
  - 本页没有标题和讲解文字，四张教材插图略微错开叠放，应按 1→4 的顺序看
  - 图中符号：
    - \(M\)：应用层报文（message）
    - \(H_t\)：传输层首部
    - \(H_n\)：网络层首部
    - \(H_1\)：链路层首部。图中下标写成 1；也可能是字母 L，即 \(H_L\) `[待确认]`
  - 源主机自上而下封装：\(M\) → \(H_tM\) → \(H_nH_tM\) → \(H_1H_nH_tM\)
  - 四步：
    1. **源主机到交换机**（Delivery from Source to Switch）：源主机拥有全部五层；链路层交换机只有链路层和物理层
    2. **交换机到路由器**（Delivery from Switch to Router）：交换机按链路层转发，帧仍是 \(H_1H_nH_tM\)。图注可见 “FIGURE I.33” `[图号待确认，有可能是 1.33]`
    3. **路由器到交换机**（Delivery from Router to Switch）：路由器的协议栈到网络层为止。进入与离开路由器时，链路首部 \(H_1\) 在图上颜色不同，表示换了新链路后链路首部被更换，\(H_nH_tM\) 继续前传。图注 “FIGURE I.34” `[待确认]`
    4. **交换机到目的主机**（Delivery from Switch to Destination）：目的主机从链路层一直拆到应用层。图注 “FIGURE I.35” `[待确认]`
- **图表/图片说明**：四张结构相同的网络图。左上是源主机（Source）及其五层协议栈，左下是目的主机（Destination）。路径上有两台链路层交换机（Link-layer Switch）和右侧一台路由器（Router）。交换机框内只有 Link 和 Physical；路由器框内有 Network、Link、Physical。绿色箭头标出当前这一跳。第 1 张图还画出源主机逐层添加 \(M\)、\(H_t\)、\(H_n\)、\(H_1\)。
- **难点标记**：⭐⭐⭐ 难点
- **预习疑问**：路由器会不会看见、或者有必要看见应用层的 \(M\)？如果链路加密把整帧加密，路由器还能不能读到自己的控制信息？

### 第 12 页：物理层或数据链路层的安全

- **原文标题/关键词**：Security at the Physical or Data Link Layers；point-to-point；heterogeneous networks；link-level encryption；intermediate node；key management
- **一句话总结**：链路加密能保护每一段点到点链路，但每到一个中间节点就要解密，保护到不了整条异构路径。
- **中文翻译/要点**：
  - 优点：提供安全的点到点通信（secure point-to-point communication）
  - 缺点：
    - 保护无法延伸到异构网络（heterogeneous networks）之上
    - 若使用链路级加密（link-level encryption），每条链路两端都要配备加密设备
    - 报文在每个中间节点都要先解密，以便上层协议读到自己的控制信息，然后再加密
    - 密钥管理（key management）非常复杂
    - 因为每个设备上都有一次解密，报文在每个中间节点都暴露给攻击。原文称这是严重缺点
  - 页上的讨论题：谁需要安全的点到点通信？（Who needs secure point-to-point communication?）
- **图表/图片说明**：无。第 13–14 页的对照图把本层机制标成：链路加密（link encryption）、MAC 地址过滤（MAC address filtering），并在网络接入层旁列出 `[CHAP, EAP]`
- **难点标记**：⭐⭐⭐ 难点
- **预习疑问**：谁需要这种 “每一跳都单独保护” 的点到点通信？长路径上的中间路由器算受益者还是风险点？

### 第 13 页：互联网层的安全

- **原文标题/关键词**：Security at the Internet Layer；transparent；single tunnel；TCP, UDP, SNMP；operating system；compatible versions；VPN with IPsec
- **一句话总结**：IPsec 在互联网层做一条隧道，应用不用改；代价是要动操作系统，并且两端软件必须兼容。
- **中文翻译/要点**：
  - 优点：
    - 对用户和应用透明（transparent）。一条隧道（tunnel）保护设备之间的全部通信，不区分流量类型（TCP、UDP、SNMP）或应用（电子邮件、客户端-服务器、数据库）
    - 安全软件由有经验的系统管理员安装和维护，混入恶意代码的可能性较低
  - 缺点：
    - 互联网层安全要求修改底层操作系统
    - 所有通信主机必须使用兼容版本的网络安全软件
  - 例子：使用 IPsec 的 VPN（VPN with IPsec）
  - 对照图在互联网层右侧写的机制是：IP AH、IP ESP
    - AH：认证首部（Authentication Header）
    - ESP：封装安全载荷（Encapsulating Security Payload）
- **图表/图片说明**：左侧是 OSI 七层（应用、表示、会话、传输、网络、数据链路、物理）。中间是互联网四层：进程/应用（Process/Application，合并 OSI 上三层）、传输（Transport）、互联网（Internet）、网络接入（Network access）。右侧按层列出安全机制。与本页直接对应的是互联网层上的 “IP AH, IP ESP”。同一张图也画出了其他层的机制，完整名单见下一页的图示说明。
- **难点标记**：⭐⭐⭐ 难点
- **预习疑问**：一条 IPsec 隧道可以同时保护网页、邮件和数据库。管理员少装了哪一端的兼容软件，这条透明保护还会成立吗？

### 第 14 页：传输层的安全

- **原文标题/关键词**：Security at the Transport Layer；security aware；function calls；transport security library；SSL VPN gateway；proxy；VPN tunnel using SSL
- **一句话总结**：传输层安全通常要应用主动调用；若改成边界上的 SSL VPN 网关，内部应用可以不感知安全。
- **中文翻译/要点**：
  - 缺点：
    - 每个应用都必须 “安全感知”（security aware），也就是调用相应的安全函数。安全是一个应用、一个应用地加上去的
    - 传输安全库要由系统管理员安装和维护，主机上的应用才能使用
  - 优点：
    - 运行在内部主机上的应用不必安全感知
    - 有的企业在公司网络边缘部署专用 SSL VPN 网关，作为内部应用的代理（proxy），例如电子邮件和文件服务器
  - 例子：使用 SSL 的 VPN 隧道（VPN tunnel using SSL）
  - 页上的图与第 13 页相同。与传输层相邻、标在进程/应用层下沿的机制包括：安全 RPC（secure RPC）、SASL、SSH、SSL/TLS。更靠上的还有 S/MIME、S-HTTP、安全 Telnet（secure TELNET）
- **图表/图片说明**：与第 13 页为同一张对照图。右侧完整名单按图中位置大致为：
  - 进程/应用层上沿：S/MIME、S-HTTP、secure TELNET
  - 进程/应用层下沿至传输层附近：secure RPC、SASL、SSH、SSL/TLS
  - 互联网层：IP AH、IP ESP
  - 网络接入层：`[CHAP, EAP]`、链路加密、MAC 地址过滤
  - 图中 SSL/TLS 画在应用与传输的交界附近，而本页正文把 SSL VPN 当作传输层安全的例子。两边不要背成矛盾，见本节末的说明
- **难点标记**：⭐⭐⭐ 难点
- **预习疑问**：同一页既说 “每个应用都必须安全感知”，又说 “内部主机上的应用不必安全感知”。这两种说法各对应哪一种部署？

> 两种说法都在原文里，差别在部署位置：应用自己调用传输层安全库时，应用必须安全感知；公司边界用 SSL VPN 网关代理内部邮件、文件服务时，内部应用不必安全感知。

### 第 15 页：传输层 VPN 与 IP 层 VPN

- **原文标题/关键词**：VPN at Transport Layer vs IP Layer；SSH client；SSH server；TCP port 22；Transport layer；Mail client；Mail server (need not be security aware)；Require proper mail ports binding；IPsec client；IPsec VPN；Internet layer；Does not require proper mail ports binding
- **一句话总结**：SSH 在传输层、要占用 TCP 22，并且邮件端口必须绑定正确；IPsec 在互联网层，不要求按邮件端口绑定。
- **中文翻译/要点**：
  - **上半：传输层方案**
    - 左侧 SSH 客户端（SSH client）
    - 右侧 SSH 服务器（SSH server）
    - 中间标注传输层（Transport layer），并标出 TCP 端口 22（TCP port 22）
    - 下方邮件客户端（Mail client）通向邮件服务器
    - 邮件服务器 “不必安全感知”（need not be security aware）
    - 但 “要求正确的邮件端口绑定”（Require proper mail ports binding）
  - **下半：IP 层方案**
    - 左侧 IPsec 客户端（IPsec client）
    - 右侧 IPsec VPN
    - 中间标注互联网层（Internet layer）
    - 邮件客户端同样出现
    - 标注为 “不要求正确的邮件端口绑定”（Does not require proper mail ports binding）
- **图表/图片说明**：示意图，不是协议字段图。左侧是台式机和邮件客户端界面，右侧是塔式服务器。上下两行结构平行，用来对比端口绑定，没有给出配置命令。
- **难点标记**：⭐⭐⭐ 难点
- **预习疑问**：邮件服务器本身可以不实现加密，为什么传输层方案仍然要 “把邮件端口绑定对”？

### 第 16 页：应用层的安全

- **原文标题/关键词**：Security at the Application Layer；no changes in the operating system；end-to-end security；cryptographic computations；inexperienced users；malicious code；e-banking login
- **一句话总结**：应用层安全只装一个安全应用，端到端密码学可以做在操作系统之外，但常由不熟练的用户安装，恶意代码风险高。
- **中文翻译/要点**：
  - 优点：
    - 不必修改操作系统，只需要安装安全应用
    - 端到端安全（end-to-end security）更好，因为建立过程和密码学计算都在操作系统之外完成
    - 安全功能可以按该应用的需求精确设计
  - 缺点：
    - 通信进程之间的协商和建立过程可能更复杂
    - 安全应用常常由缺乏经验的用户安装，混入恶意代码的危险相当高
  - 例子：网上银行登录（e-banking login）
  - 可与第 13 页对照：互联网层软件多由管理员维护，恶意代码风险被讲义说成较低；应用层则相反
- **图表/图片说明**：无。第 13–14 页的图把 S/MIME、S-HTTP、secure TELNET 标在进程/应用层
- **难点标记**：⭐⭐ 重点
- **预习疑问**：网银登录保护的是 “这一个应用”，还是这台电脑上的全部流量？这和 IPsec 隧道的保护范围有何不同？

### 跨页对照：四层安全（第 12–16 页）

| 层次 | 本讲例子 | 保护特点 | 主要代价 |
| --- | --- | --- | --- |
| 物理 / 数据链路 | 链路加密；MAC 地址过滤；图中还有 CHAP、EAP | 点到点 | 不能跨异构网；每跳两端都要加密设备；中间节点解密，明文暴露；密钥管理复杂 |
| 互联网 | IPsec VPN；IP AH、IP ESP | 对用户和应用透明；一条隧道覆盖多种流量 | 要改操作系统；各主机安全软件版本必须兼容 |
| 传输 | SSL VPN；图中的 SSL/TLS、SSH；第 15 页的 TCP 22 | 边界网关可代理内部应用，使内部应用不感知安全 | 应用直接使用时必须安全感知；安全库由管理员维护；SSH 方案要求邮件端口绑定正确 |
| 应用 | 网银登录；图中的 S/MIME、S-HTTP、secure TELNET | 不改操作系统；密码学在操作系统之外；可按应用定制 | 协商更复杂；用户自行安装，恶意代码风险高 |

## 6. 术语表

| 英文/原文 | 中文译名 | 解释 | 出现页码 |
| --- | --- | --- | --- |
| communication network | 通信网络 | 以电子形式交换信息的基础设施 | 第 3 页 |
| physical / logical infrastructure | 物理 / 逻辑基础设施 | 前者是线路和设备，后者是协议 | 第 3 页 |
| protocol suite | 协议族 | 一组相互配合的通信协议；TCP/IP 是协议族 | 第 5 页 |
| internetworking | 网络互连 | 使不同网络中的主机能够通信 | 第 5、7 页 |
| Host to network / Network Access / Network Interface | 主机到网络层 / 网络接入层 / 网络接口层 | 本讲对 TCP/IP 最底层的三种叫法 | 第 5、6、10 页 |
| LLC (Logical Link Control) | 逻辑链路控制 | IEEE 802.2 子层；原文还把它写成同一 LAN 内的路由 | 第 6 页 |
| MAC (Medium Access Control) | 介质访问控制 | 隐藏介质种类、拓扑和介质访问方式 | 第 6 页 |
| Ethernet / IEEE 802.3 | 以太网 | 本讲举出的一种介质控制技术 | 第 6 页 |
| token ring / IEEE 802.5 | 令牌环 | 本讲举出的另一种介质控制技术 | 第 6 页 |
| routing | 路由、选路 | 决定下一跳，不要求知道整条路径 | 第 7 页 |
| IPv4 | 网际协议第 4 版 | 本讲强调其地址为 4 字节 | 第 7 页 |
| Network ID / Host ID | 网络号 / 主机号 | 第 7 页图注：前 8 位与后 24 位 | 第 7 页 |
| TCP | 传输控制协议 | 传输层协议；与 “可靠传送” 的对应见第 8 页 `[待确认]` | 第 8、10 页 |
| UDP | 用户数据报协议 | 传输层协议；与 “不可靠传送” 的对应见第 8 页 `[待确认]` | 第 8、10 页 |
| process/application layer | 进程/应用层 | TCP/IP 应用层的另一说法，覆盖 OSI 第 5–7 层 | 第 9 页 |
| ARP / RARP | 地址解析协议 / 反向地址解析协议 | 图画在互联网层与网络接口层之间 | 第 10 页 |
| PPP / SLIP | 点到点协议 / 串行线路接口协议 | 网络接口层协议 | 第 10 页 |
| encapsulation | 封装 | 第 11 页图所示：下到一层就加一个首部 | 第 11 页 |
| link-layer switch | 链路层交换机 | 协议栈只到链路层和物理层 | 第 11 页 |
| link-level encryption | 链路级加密 | 每条链路两端加密，中间节点解密再加密 | 第 12 页 |
| heterogeneous network | 异构网络 | 链路层保护无法延伸穿过的网络环境 | 第 12 页 |
| key management | 密钥管理 | 链路加密方案中被原文明说为极其复杂 | 第 12 页 |
| transparent | 透明 | 用户和应用不必感知安全机制 | 第 13 页 |
| tunnel | 隧道 | 一条通道保护设备间的全部通信 | 第 13 页 |
| VPN | 虚拟专用网 | 本讲例子：IPsec VPN、SSL VPN | 第 13–15 页 |
| IPsec | IP 安全协议 | 互联网层安全协议 | 第 10、13、15 页 |
| AH / ESP | 认证首部 / 封装安全载荷 | 对照图写在互联网层的两种 IP 安全机制 | 第 13 页 |
| security aware | 安全感知 | 应用必须主动调用安全函数 | 第 14 页 |
| SSL / TLS | 安全套接字层 / 传输层安全 | 传输层安全及 SSL VPN 的例子；图中位置靠近应用与传输交界 | 第 14 页 |
| SSL VPN gateway | SSL VPN 网关 | 放在企业网边缘，代理内部应用 | 第 14 页 |
| proxy | 代理 | 网关代表内部邮件、文件服务器对外提供受保护访问 | 第 14 页 |
| SSH | 安全外壳 | 第 15 页的传输层 VPN 例子，使用 TCP 端口 22 | 第 14、15 页 |
| port binding | 端口绑定 | 传输层方案要求邮件端口绑定正确；IPsec 不要求 | 第 15 页 |
| end-to-end security | 端到端安全 | 应用层安全的优点：建立和密码学计算在操作系统之外 | 第 16 页 |
| S/MIME | 安全多用途互联网邮件扩展 | 对照图中的应用层邮件安全机制 | 第 13–14 页 |
| S-HTTP | 安全超文本传输协议 | 图中的应用层机制；不要写成今天的 HTTPS | 第 13–14 页 |
| CHAP / EAP | 质询握手认证协议 / 可扩展认证协议 | 对照图中放在网络接入层，并加了方括号 | 第 13–14 页 |
| SASL | 简单认证与安全层 | 对照图中靠近应用/传输交界的机制 | 第 13–14 页 |

第 10 页协议图中的 DNS、DHCP、SNMP、FTP、SMTP、HTTP、BGP、OSPF 等，只在该页列出名称。本表不逐个展开。

## 7. 重点、难点与易错点

### 重点

- TCP/IP 四层及最底层的三个别名：Host to network、Network Access、Network Interface
- 互联网层只决定下一跳，IPv4 地址长度为 4 字节
- 第 11 页的封装顺序 \(M \rightarrow H_tM \rightarrow H_nH_tM \rightarrow H_1H_nH_tM\)，以及交换机、路由器各自能看到的层
- 四层安全的取舍：点到点、对应用透明、要不要改操作系统、由管理员还是用户安装
- 第 15 页的唯一对比结论：传输层 SSH 要求正确的邮件端口绑定，IPsec 不要求

### 难点

- 链路加密为什么必须在中间节点解密：上层协议要读自己的控制信息。这正好解释它 “严重暴露” 的原因
- 第 14 页两句看似相反的话：应用必须安全感知，内部应用又可以不感知。前者是应用直接调用安全库，后者是边缘 SSL VPN 网关做代理
- SSL/TLS 在对照图里靠近应用层下沿，正文却把 SSL VPN 放在传输层。记住 “图上的位置” 和 “本讲对 SSL VPN 的归类” 即可
- 路由器更换的是链路首部 \(H_1\)，不是整个 \(H_nH_tM\)

### 易错点

- 不要把 TCP/IP 四层背成 OSI 七层。应用层在本讲里已经包含 OSI 第 5–7 层
- 不要把第 7 页的 “8 位网络号 + 24 位主机号” 当成标准分类编址例题。示例地址 `227.82.157.177` 的分类属性与图注不一致 `[待确认]`
- 不要在第 8 页原文之外，把 “TCP = 可靠、UDP = 不可靠” 写成幻灯片原句
- 第 6 页把同一 LAN 内的路由归给 LLC `[待确认]`，与常见的 MAC 转发说法可能不同
- S-HTTP 不是 HTTPS。IPsec 不是应用层协议，网银登录也不是 IPsec
- 第 13 页说管理员维护降低恶意代码风险，第 16 页说用户安装提高恶意代码风险。比较的是安装者，不是密码算法本身
- 第 15 页的邮件服务器 “不必安全感知” 写在传输层方案上，不要记成 “只有 IPsec 才允许服务器不加密”

## 8. 课前预习问题

### 基础理解

1. 通信网络的物理基础设施和逻辑基础设施各指什么？只有导线和路由器，没有协议，算不算本讲定义的通信网络？
2. 按本讲的 TCP/IP 模型，自下而上四层分别叫什么？最底层还有哪两个别名？
3. IPv4 地址是几字节？把 `227.82.157.177` 按图写成四段二进制时，第一段为什么是 `11100011`？

### 重点掌握

4. 链路级加密在每个中间节点解密，原文给出的直接原因是什么？这带来哪一个 “严重缺点”？
5. 为什么说 IPsec 对用户和应用透明？透明的同时，操作系统和软件版本要满足什么条件？
6. SSL VPN 网关放在企业网边缘并充当代理时，内部邮件服务器为什么可以不安全感知？
7. 第 15 页中，SSH 方案和 IPsec 方案对邮件端口绑定的要求有何不同？SSH 使用的 TCP 端口号是多少？

### 拓展思考

8. 若目标是 “不改操作系统，只让用户安装一个安全程序”，本讲会把方案放在哪一层？它交换来的风险是什么？
9. 结合第 11 页：路由器处理到网络层。如果安全只做在应用层，路由器能否借此读到应用数据的内容？这和链路加密 “中间节点必须看见控制信息” 有什么差别？

## 9. 自测题

### 选择题

1. 按第 5 页的 TCP/IP 模型，自下而上的顺序是：
   - A. 应用、传输、互联网、主机到网络
   - B. 主机到网络、互联网、传输、应用
   - C. 物理、数据链路、网络、传输、会话、表示、应用
   - D. 主机到网络、传输、互联网、应用

2. 第 7 页关于 IPv4 地址的说法，哪一项符合幻灯片？
   - A. 地址长度为 16 字节，例子是 `227.82.157.177`
   - B. 地址长度为 4 字节，例子是 `227.82.157.177`
   - C. 路由必须预先知道到达目的主机的整条路径
   - D. 互联网层只能在同一个 LAN 内转发

3. 链路级加密被本讲视为严重缺点的一点是：
   - A. 必须修改每台主机的操作系统
   - B. 报文在每个中间节点解密，从而暴露给攻击
   - C. 每个应用都要调用安全函数
   - D. 只能由缺乏经验的用户安装

4. 第 15 页对两种 VPN 的对比，正确的是：
   - A. SSH 工作在互联网层，且不使用端口号
   - B. IPsec 工作在传输层，并要求 TCP 端口 22
   - C. SSH 方案要求正确的邮件端口绑定，IPsec 方案不要求
   - D. 两种方案都要求邮件服务器自己实现全部密码学功能

5. 第 16 页认为应用层安全的优点包括：
   - A. 不必修改操作系统，安全功能可以按该应用的需求来做
   - B. 一条隧道自动保护该主机的全部流量，包括数据库和 SNMP
   - C. 中间每个路由器都持有应用层密钥
   - D. 由不熟练用户安装，因此恶意代码风险更低

### 简答题

1. 用第 13 页的两点优点、两点限制，说明 “VPN with IPsec” 适合保护什么、不适合忽略什么。
2. 第 14 页为什么同时写出 “应用必须安全感知” 和 “内部主机上的应用不必安全感知”？各指哪一种做法？
3. 根据第 11 页，源主机发出前数据单元的组成是什么？链路层交换机和路由器分别处理到哪一层？路由器离开原链路时，哪一部分首部会改变？

<details>
<summary>查看答案与简答要点</summary>

**选择题**

1. B。图中自下而上为 Host to network、Internet、Transport、Application。C 是 OSI 七层。
2. B。原文写明路由基于 4 字节 IPv4 地址，图中的地址是 `227.82.157.177`。A 的长度错误；C 与 “不必知道整条路径” 相反；D 把互联网层说成了局域网。
3. B。A 是互联网层的限制，C 是传输层的限制，D 把第 16 页的风险说反了。
4. C。SSH 在传输层，图上标的是 TCP port 22，并要求邮件端口绑定；IPsec 在互联网层，不要求该绑定。
5. A。B 是第 13 页互联网层隧道的特点。D 与原文相反：用户安装使恶意代码风险升高。

**简答题**

1. 优点：对用户和应用透明，一条隧道覆盖 TCP、UDP、SNMP 以及邮件、客户端-服务器、数据库等流量；软件由管理员维护，恶意代码风险相对低。限制：要修改底层操作系统；通信各方必须使用兼容的网络安全软件。因此它适合一次保护两台设备之间的多种流量，但不能忽略系统改动和版本兼容。
2. “必须安全感知” 指每个应用自己调用传输层安全函数，安全要一个应用一个应用地加。“不必安全感知” 指企业在网络边缘部署 SSL VPN 网关，网关代理内部的邮件、文件服务器，内部应用不用自己实现安全。
3. 源主机送到链路上的单元是 \(H_1H_nH_tM\)（链路首部下标 `[待确认]`）。交换机只有链路层和物理层。路由器处理到网络层。换到下一条链路时改变的是链路首部 \(H_1\)，\(H_nH_tM\) 继续转发。

</details>

## 10. 一页总结

课前三分钟只看这一节即可。

- [ ] 通信网络 = 线路、路由器等物理设施 + 赋予二进制含义的协议
- [ ] 本讲的 TCP/IP 四层自下而上：主机到网络（又称网络接入/网络接口）、互联网、传输、应用；应用层覆盖 OSI 第 5–7 层
- [ ] 互联网层用 4 字节 IPv4 地址选下一跳，不要求知道整条路径
- [ ] 发送时逐层加首部 \(H_t\)、\(H_n\)、\(H_1\)；交换机只到链路层，路由器到网络层并更换链路首部
- [ ] 链路加密是点到点的，每条链路两端都要设备，中间节点为了读控制信息必须解密，因此明文会暴露
- [ ] IPsec 在互联网层，一条隧道对应用透明，但要改操作系统且两端软件兼容
- [ ] 传输层的 SSL/SSH 通常要应用调用安全函数；边缘 SSL VPN 网关可以让内部应用不感知安全。SSH 要绑定好邮件端口并使用 TCP 22，IPsec 不要求这种端口绑定
- [ ] 应用层安全不改操作系统，能按应用定制（如网银登录），但协商更复杂，且用户自行安装时恶意代码风险高
