# Uniswap V4 流动性移除工具

一个简单的网页工具，用于生成 Uniswap V4 移除流动性所需的参数。

## 功能

- 输入流动性池参数（Token ID、货币地址、接收者地址、流动性数量）
- 自动生成 `unlockData` 和 `deadline` 参数
- 支持直接复制生成的十六进制数据

## 使用方法

1. 访问 [GitHub Pages 部署地址](https://your-username.github.io/uniswap-v4-liquidity-remover/)
2. 填写以下参数：
   - **Token ID**: 您的 NFT 位置 ID
   - **Currency 0**: 第一个代币的合约地址
   - **Currency 1**: 第二个代币的合约地址  
   - **Recipient**: 接收代币的地址
   - **Liquidity**: 要移除的流动性数量
3. 点击"生成参数"按钮
4. 复制生成的 `unlockData` 和 `deadline` 参数

## 技术实现

- 使用 `ethers.js` 进行 ABI 编码
- 支持 Uniswap V4 的 DECREASE_LIQUIDITY 和 TAKE_PAIR 操作
- 自动生成当前时间 + 10 分钟的 deadline

## 本地运行

```bash
# 克隆仓库
git clone https://github.com/your-username/uniswap-v4-liquidity-remover.git

# 进入目录
cd uniswap-v4-liquidity-remover

# 启动本地服务器
python -m http.server 8000

# 访问 http://localhost:8000/liquidity-generator.html
```

## 注意事项

- 请确保输入的地址格式正确（以 0x 开头的 42 位十六进制字符串）
- Token ID 和 Liquidity 必须是有效的数字
- 生成的参数仅用于 Uniswap V4 协议

## 许可证

MIT License