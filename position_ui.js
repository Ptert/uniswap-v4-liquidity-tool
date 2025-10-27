// 网络配置
const networkConfigs = {
    base: {
        rpcUrl: 'https://mainnet.base.org',
        contracts: {
            USDC: '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA',
            ETH: '0x4200000000000000000000000000000000000006',
            UNISWAP_V4_UNIVERSAL_ROUTER: '0x198EF79F1F515F02dFE9e3115eD9fC07183f02fC',
            UNISWAP_V4_POSITION_MANAGER: '0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1',
            UNISWAP_V4_NFT_POSITION_MANAGER: '0x8AA21694e2e0463bDF70A9f1EFcF7Fd6D9a1FE6F',
            UNISWAP_V4_STATE_VIEW: '0x1B8eea9315bE495187D875DA315F0eb3af46De95',
            UNISWAP_V4_POOL_MANAGER: '0x64255ed21366DB43d89736EE48928b890A84E2Cb'
        }
    },
    ethereum: {
        rpcUrl: 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', // 使用公共Infura端点
        contracts: {
            USDC: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
            ETH: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
            UNISWAP_V4_UNIVERSAL_ROUTER: '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD',
            UNISWAP_V4_POSITION_MANAGER: '0x8E0E20Ec74C1f0D2Fb7CAaA5B64579CbE385eAC2',
            UNISWAP_V4_NFT_POSITION_MANAGER: '0xC36442b4a4522E871399CD717aBDD847Ab11FE88',
            UNISWAP_V4_STATE_VIEW: '0x42A768080E2EE0D4A9C0D4Bc94E1C9e5A6B5603e',
            UNISWAP_V4_POOL_MANAGER: '0x2D98E2FA9da15aa6dC9581AB097Ced7af697CB92'
        }
    }
};

// ABI定义
const STATE_VIEW_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "currency0",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "currency1",
                        "type": "address"
                    },
                    {
                        "internalType": "uint24",
                        "name": "fee",
                        "type": "uint24"
                    },
                    {
                        "internalType": "int24",
                        "name": "tickSpacing",
                        "type": "int24"
                    },
                    {
                        "internalType": "address",
                        "name": "hooks",
                        "type": "address"
                    }
                ],
                "internalType": "struct PoolKey",
                "name": "key",
                "type": "tuple"
            }
        ],
        "name": "getSlot0",
        "outputs": [
            {
                "internalType": "uint160",
                "name": "sqrtPriceX96",
                "type": "uint160"
            },
            {
                "internalType": "int24",
                "name": "tick",
                "type": "int24"
            },
            {
                "internalType": "uint8",
                "name": "protocolFee",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
];

const NFT_POSITION_MANAGER_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "token0",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "token1",
                        "type": "address"
                    },
                    {
                        "internalType": "uint24",
                        "name": "fee",
                        "type": "uint24"
                    },
                    {
                        "internalType": "int24",
                        "name": "tickLower",
                        "type": "int24"
                    },
                    {
                        "internalType": "int24",
                        "name": "tickUpper",
                        "type": "int24"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount0Desired",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount1Desired",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount0Min",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount1Min",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "recipient",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "deadline",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct INonfungiblePositionManager.MintParams",
                "name": "params",
                "type": "tuple"
            }
        ],
        "name": "mint",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "internalType": "uint128",
                "name": "liquidity",
                "type": "uint128"
            },
            {
                "internalType": "uint256",
                "name": "amount0",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amount1",
                "type": "uint256"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    }
];

const ERC20_ABI = [
    {
        "constant": false,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
];

// 全局变量
let web3;
let currentNetwork = 'base';
let currentAccount;
let currentPrice = 0;

// 工具函数
function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    errorAlert.textContent = message;
    errorAlert.style.display = 'block';
    setTimeout(() => {
        errorAlert.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    const successAlert = document.getElementById('successAlert');
    successAlert.textContent = message;
    successAlert.style.display = 'block';
    setTimeout(() => {
        successAlert.style.display = 'none';
    }, 5000);
}

function showLoading(show) {
    document.getElementById('loadingIndicator').style.display = show ? 'block' : 'none';
    document.getElementById('createPositionBtn').disabled = show;
}

// 计算价格从sqrt价格
function calculatePriceFromSqrtPriceX96(sqrtPriceX96, decimals0 = 18, decimals1 = 6) {
    const numerator = BigInt(sqrtPriceX96) ** 2n;
    const denominator = 2n ** 192n;
    const price = Number(numerator * 10n ** BigInt(decimals0) / denominator) / 10 ** decimals1;
    return price;
}

// 价格转tick
function priceToTick(price, decimals0 = 18, decimals1 = 6) {
    const decimalAdjustedPrice = price * (10 ** decimals1 / 10 ** decimals0);
    return Math.floor(Math.log(decimalAdjustedPrice) / Math.log(1.0001));
}

// tick转价格
function tickToPrice(tick, decimals0 = 18, decimals1 = 6) {
    const price = 1.0001 ** tick;
    return price * (10 ** decimals0 / 10 ** decimals1);
}

// 获取tick范围
function getTickRange(currentTick, percentage) {
    const tickRange = Math.floor(Math.log(1 + percentage) / Math.log(1.0001));
    return {
        lowerTick: Math.floor(currentTick - tickRange),
        upperTick: Math.floor(currentTick + tickRange)
    };
}

// 初始化Web3
function initWeb3() {
    try {
        const networkConfig = networkConfigs[currentNetwork];
        web3 = new Web3(new Web3.providers.HttpProvider(networkConfig.rpcUrl));
        return true;
    } catch (error) {
        showError(`初始化Web3失败: ${error.message}`);
        return false;
    }
}

// 验证和格式化私钥
function validatePrivateKey(privateKey) {
    let formattedKey = privateKey.trim();
    if (!formattedKey.startsWith('0x')) {
        formattedKey = '0x' + formattedKey;
    }
    
    if (!/^0x[0-9a-fA-F]{64}$/.test(formattedKey)) {
        throw new Error('私钥格式不正确，应为64位十六进制字符串，可选前缀0x');
    }
    
    return formattedKey;
}

// 创建池子键
function createPoolKey(token0, token1, feeTier) {
    const networkConfig = networkConfigs[currentNetwork];
    const tokenAddresses = {
        eth: networkConfig.contracts.ETH,
        usdc: networkConfig.contracts.USDC
    };

    return {
        currency0: tokenAddresses[token0],
        currency1: tokenAddresses[token1],
        fee: parseInt(feeTier),
        tickSpacing: 10,
        hooks: '0x0000000000000000000000000000000000000000'
    };
}

// 获取当前价格
async function getCurrentPrice() {
    try {
        showLoading(true);
        
        const token0 = document.getElementById('token0Select').value;
        const token1 = document.getElementById('token1Select').value;
        const feeTier = document.getElementById('feeTierSelect').value;
        
        if (token0 === token1) {
            showError('代币0和代币1不能相同');
            showLoading(false);
            return;
        }
        
        const poolKey = createPoolKey(token0, token1, feeTier);
        const networkConfig = networkConfigs[currentNetwork];
        
        const stateViewContract = new web3.eth.Contract(
            STATE_VIEW_ABI,
            networkConfig.contracts.UNISWAP_V4_STATE_VIEW
        );
        
        const slot0 = await stateViewContract.methods.getSlot0(poolKey).call();
        const sqrtPriceX96 = slot0.sqrtPriceX96;
        const tick = parseInt(slot0.tick);
        
        // 根据代币对调整小数位
        let decimals0 = token0 === 'eth' ? 18 : 6;
        let decimals1 = token1 === 'eth' ? 18 : 6;
        
        currentPrice = calculatePriceFromSqrtPriceX96(sqrtPriceX96, decimals0, decimals1);
        document.getElementById('currentPriceDisplay').value = currentPrice.toFixed(6);
        
        // 更新价格范围
        updatePriceRange();
        
        showSuccess('成功获取当前价格');
        showLoading(false);
    } catch (error) {
        showError(`获取价格失败: ${error.message}`);
        showLoading(false);
    }
}

// 更新价格范围
function updatePriceRange() {
    if (currentPrice <= 0) {
        showError('请先获取当前价格');
        return;
    }
    
    const percentage = parseFloat(document.getElementById('priceRangeSlider').value) / 100;
    document.getElementById('priceRangeValue').textContent = `${percentage * 100}%`;
    
    const lowerPrice = currentPrice * (1 - percentage);
    const upperPrice = currentPrice * (1 + percentage);
    
    document.getElementById('lowerPriceInput').value = lowerPrice.toFixed(6);
    document.getElementById('upperPriceInput').value = upperPrice.toFixed(6);
}

// 创建头寸
async function createPosition() {
    try {
        showLoading(true);
        
        // 获取表单数据
        const privateKey = document.getElementById('privateKeyInput').value;
        if (!privateKey) {
            showError('请输入私钥');
            showLoading(false);
            return;
        }
        
        // 设置账户
        try {
            const account = web3.eth.accounts.privateKeyToAccount(privateKey);
            currentAccount = account.address;
            web3.eth.accounts.wallet.add(account);
            web3.eth.defaultAccount = currentAccount;
        } catch (error) {
            showError(`私钥无效: ${error.message}`);
            showLoading(false);
            return;
        }
        
        const token0 = document.getElementById('token0Select').value;
        const token1 = document.getElementById('token1Select').value;
        const feeTier = document.getElementById('feeTierSelect').value;
        
        if (token0 === token1) {
            showError('代币0和代币1不能相同');
            showLoading(false);
            return;
        }
        
        if (currentPrice <= 0) {
            showError('请先获取当前价格');
            showLoading(false);
            return;
        }
        
        const amount0 = parseFloat(document.getElementById('token0AmountInput').value);
        const amount1 = parseFloat(document.getElementById('token1AmountInput').value);
        
        if (isNaN(amount0) || amount0 <= 0 || isNaN(amount1) || amount1 <= 0) {
            showError('请输入有效的代币数量');
            showLoading(false);
            return;
        }
        
        const slippage = parseFloat(document.getElementById('slippageInput').value) / 100;
        if (isNaN(slippage) || slippage <= 0) {
            showError('请输入有效的滑点容忍度');
            showLoading(false);
            return;
        }
        
        const percentage = parseFloat(document.getElementById('priceRangeSlider').value) / 100;
        
        // 获取网络配置
        const networkConfig = networkConfigs[currentNetwork];
        
        // 创建合约实例
        const nftPositionManagerContract = new web3.eth.Contract(
            NFT_POSITION_MANAGER_ABI,
            networkConfig.contracts.UNISWAP_V4_NFT_POSITION_MANAGER
        );
        
        // 获取代币地址
        const token0Address = networkConfig.contracts[token0.toUpperCase()];
        const token1Address = networkConfig.contracts[token1.toUpperCase()];
        
        // 计算tick范围
        const token0Decimals = token0 === 'eth' ? 18 : 6;
        const token1Decimals = token1 === 'eth' ? 18 : 6;
        const currentTick = priceToTick(currentPrice, token0Decimals, token1Decimals);
        const { lowerTick, upperTick } = getTickRange(currentTick, percentage);
        
        // 计算最小数量
        const amount0Min = Math.floor(amount0 * (1 - slippage) * (10 ** token0Decimals));
        const amount1Min = Math.floor(amount1 * (1 - slippage) * (10 ** token1Decimals));
        const amount0Desired = Math.floor(amount0 * (10 ** token0Decimals));
        const amount1Desired = Math.floor(amount1 * (10 ** token1Decimals));
        
        // 如果使用USDC，需要先授权
        if (token0 === 'usdc' || token1 === 'usdc') {
            const usdcContract = new web3.eth.Contract(
                ERC20_ABI,
                networkConfig.contracts.USDC
            );
            
            showSuccess('正在授权USDC...');
            
            // 授权USDC
            const approvalAmount = '115792089237316195423570985008687907853269984665640564039457584007913129639935'; // uint256 max
            await usdcContract.methods
                .approve(networkConfig.contracts.UNISWAP_V4_NFT_POSITION_MANAGER, approvalAmount)
                .send({ from: currentAccount, gas: 200000 });
                
            showSuccess('USDC授权成功');
        }
        
        // 准备交易参数
        const mintParams = {
            token0: token0Address,
            token1: token1Address,
            fee: parseInt(feeTier),
            tickLower: lowerTick,
            tickUpper: upperTick,
            amount0Desired: amount0Desired.toString(),
            amount1Desired: amount1Desired.toString(),
            amount0Min: amount0Min.toString(),
            amount1Min: amount1Min.toString(),
            recipient: currentAccount,
            deadline: Math.floor(Date.now() / 1000) + 3600 // 1小时后过期
        };
        
        // 发送交易
        showSuccess('正在创建头寸...');
        
        let txOptions = {
            from: currentAccount,
            gas: 500000
        };
        
        // 如果使用ETH，需要添加value
        if (token0 === 'eth') {
            txOptions.value = amount0Desired.toString();
        } else if (token1 === 'eth') {
            txOptions.value = amount1Desired.toString();
        }
        
        const receipt = await nftPositionManagerContract.methods
            .mint(mintParams)
            .send(txOptions);
            
        showSuccess(`头寸创建成功! 交易哈希: ${receipt.transactionHash}`);
        showLoading(false);
    } catch (error) {
        showError(`创建头寸失败: ${error.message}`);
        showLoading(false);
    }
}

// 初始化页面
document.addEventListener('DOMContentLoaded', function() {
    // 初始化Web3
    initWeb3();
    
    // 网络选择事件
    document.getElementById('networkSelect').addEventListener('change', function() {
        currentNetwork = this.value;
        initWeb3();
        showSuccess(`已切换到${currentNetwork === 'base' ? 'Base' : '以太坊主网'}`);
    });
    
    // 价格范围滑块事件
    document.getElementById('priceRangeSlider').addEventListener('input', updatePriceRange);
    
    // 获取价格按钮事件
    document.getElementById('fetchPriceBtn').addEventListener('click', getCurrentPrice);
    
    // 创建头寸按钮事件
    document.getElementById('createPositionBtn').addEventListener('click', createPosition);
    
    // 代币选择事件
    document.getElementById('token0Select').addEventListener('change', function() {
        const token1Select = document.getElementById('token1Select');
        if (this.value === token1Select.value) {
            token1Select.value = this.value === 'eth' ? 'usdc' : 'eth';
        }
    });
    
    document.getElementById('token1Select').addEventListener('change', function() {
        const token0Select = document.getElementById('token0Select');
        if (this.value === token0Select.value) {
            token0Select.value = this.value === 'eth' ? 'usdc' : 'eth';
        }
    });
});