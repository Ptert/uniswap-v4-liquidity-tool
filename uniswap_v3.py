{
    "requestId": "1ab225ea-1cac-48ee-b49d-4ab6a3910414",
    "routing": "CLASSIC",
    "permitData": {
        "domain": {
            "name": "Permit2",
            "chainId": 56,
            "verifyingContract": "0x000000000022D473030F116dDEE9F6B43aC78BA3"
        },
        "types": {
            "PermitSingle": [
                {
                    "name": "details",
                    "type": "PermitDetails"
                },
                {
                    "name": "spender",
                    "type": "address"
                },
                {
                    "name": "sigDeadline",
                    "type": "uint256"
                }
            ],
            "PermitDetails": [
                {
                    "name": "token",
                    "type": "address"
                },
                {
                    "name": "amount",
                    "type": "uint160"
                },
                {
                    "name": "expiration",
                    "type": "uint48"
                },
                {
                    "name": "nonce",
                    "type": "uint48"
                }
            ]
        },
        "values": {
            "details": {
                "token": "0x0A43fC31a73013089DF59194872Ecae4cAe14444",
                "amount": "1461501637330902918203684832716283019655932542975",
                "expiration": "1762569562",
                "nonce": "0"
            },
            "spender": "0x1906c1d672b88cd1b9ac7593301ca990f94eae07",
            "sigDeadline": "1759979362"
        }
    },
    "permitTransaction": null,
    "quote": {
        "chainId": 56,
        "swapper": "0xAAAA44272dc658575Ba38f43C438447dDED45358",
        "tradeType": "EXACT_OUTPUT",
        "route": [
            [
                {
                    "type": "v3-pool",
                    "address": "0xeaB00687C6558Cd648ec288f58de4B0A6DE026bA",
                    "tokenIn": {
                        "address": "0x0A43fC31a73013089DF59194872Ecae4cAe14444",
                        "chainId": 56,
                        "symbol": "4",
                        "decimals": "18"
                    },
                    "tokenOut": {
                        "address": "0x55d398326f99059fF775485246999027B3197955",
                        "chainId": 56,
                        "symbol": "USDT",
                        "decimals": "18"
                    },
                    "sqrtRatioX96": "36717634978358827288069719572",
                    "liquidity": "2548450543149800359791361",
                    "tickCurrent": "-15383",
                    "fee": "10000",
                    "amountIn": "4009117989900908428626"
                },
                {
                    "type": "v3-pool",
                    "address": "0x2C3c320D49019D4f9A92352e947c7e5AcFE47D68",
                    "tokenIn": {
                        "address": "0x55d398326f99059fF775485246999027B3197955",
                        "chainId": 56,
                        "symbol": "USDT",
                        "decimals": "18"
                    },
                    "tokenOut": {
                        "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
                        "chainId": 56,
                        "symbol": "USDC",
                        "decimals": "18"
                    },
                    "sqrtRatioX96": "79245115770892442887910798519",
                    "liquidity": "21990087037177742871000648492",
                    "tickCurrent": "4",
                    "fee": "100",
                    "amountOut": "852125000000000000000"
                }
            ],
            [
                {
                    "type": "v3-pool",
                    "address": "0xFdB5DB3e5e4907d8987F3fc919BD60351e7a5563",
                    "tokenIn": {
                        "address": "0x0A43fC31a73013089DF59194872Ecae4cAe14444",
                        "chainId": 56,
                        "symbol": "4",
                        "decimals": "18"
                    },
                    "tokenOut": {
                        "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
                        "chainId": 56,
                        "symbol": "WBNB",
                        "decimals": "18"
                    },
                    "sqrtRatioX96": "1027621184194903050673407397",
                    "liquidity": "3300174200335130582185",
                    "tickCurrent": "-86907",
                    "fee": "3000",
                    "amountIn": "471075159533019164952"
                },
                {
                    "type": "v3-pool",
                    "address": "0x47a90A2d92A8367A91EfA1906bFc8c1E05bf10c4",
                    "tokenIn": {
                        "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
                        "chainId": 56,
                        "symbol": "WBNB",
                        "decimals": "18"
                    },
                    "tokenOut": {
                        "address": "0x55d398326f99059fF775485246999027B3197955",
                        "chainId": 56,
                        "symbol": "USDT",
                        "decimals": "18"
                    },
                    "sqrtRatioX96": "2222098978613532103624466304",
                    "liquidity": "1375757256552074608508534",
                    "tickCurrent": "-71482",
                    "fee": "100"
                },
                {
                    "type": "v3-pool",
                    "address": "0xcCDFcd1aaC447D5B29980f64b831c532a6a33726",
                    "tokenIn": {
                        "address": "0x55d398326f99059fF775485246999027B3197955",
                        "chainId": 56,
                        "symbol": "USDT",
                        "decimals": "18"
                    },
                    "tokenOut": {
                        "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
                        "chainId": 56,
                        "symbol": "USDC",
                        "decimals": "18"
                    },
                    "sqrtRatioX96": "79248495653859392677654834965",
                    "liquidity": "59594844262946009857298301",
                    "tickCurrent": "5",
                    "fee": "500",
                    "amountOut": "100250000000000000000"
                }
            ],
            [
                {
                    "type": "v4-pool",
                    "address": "0xfdbc2887ab2cdcdc680775821f00ba90632ae4e9e7a9d3c125d308e0a3338aa8",
                    "tokenIn": {
                        "address": "0x0A43fC31a73013089DF59194872Ecae4cAe14444",
                        "chainId": 56,
                        "symbol": "4",
                        "decimals": "18"
                    },
                    "tokenOut": {
                        "address": "0x55d398326f99059fF775485246999027B3197955",
                        "chainId": 56,
                        "symbol": "USDT",
                        "decimals": "18"
                    },
                    "sqrtRatioX96": "36763760333094427309387921113",
                    "liquidity": "66491050286746850972012",
                    "tickCurrent": "-15358",
                    "fee": "9800",
                    "tickSpacing": "196",
                    "hooks": "0x0000000000000000000000000000000000000000",
                    "amountIn": "235395607678883613345"
                },
                {
                    "type": "v4-pool",
                    "address": "0xb539a6a4cf8468fec432b99c57dc59049d61ec907c9d6789ec8e34158b214670",
                    "tokenIn": {
                        "address": "0x55d398326f99059fF775485246999027B3197955",
                        "chainId": 56,
                        "symbol": "USDT",
                        "decimals": "18"
                    },
                    "tokenOut": {
                        "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
                        "chainId": 56,
                        "symbol": "USDC",
                        "decimals": "18"
                    },
                    "sqrtRatioX96": "79242900039463824708755992781",
                    "liquidity": "20132706876095775683688358",
                    "tickCurrent": "3",
                    "fee": "5",
                    "tickSpacing": "1",
                    "hooks": "0x0000000000000000000000000000000000000000",
                    "amountOut": "50125000000000000000"
                }
            ]
        ],
        "input": {
            "amount": "4703829184152430131595",
            "token": "0x0A43fC31a73013089DF59194872Ecae4cAe14444"
        },
        "output": {
            "amount": "1000000000000000000000",
            "token": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
            "recipient": "0xAAAA44272dc658575Ba38f43C438447dDED45358"
        },
        "slippage": 0.5,
        "priceImpact": 1.03,
        "gasFee": "70655100000000",
        "gasFeeUSD": "0.059880390564931521",
        "gasFeeQuote": "279991809117700946",
        "gasUseEstimate": "471034",
        "routeString": "[V3] 85.00% = 4 -- 1% [0xeaB00687C6558Cd648ec288f58de4B0A6DE026bA]USDT -- 0.01% [0x2C3c320D49019D4f9A92352e947c7e5AcFE47D68]USDC, [V3] 10.00% = 4 -- 0.3% [0xFdB5DB3e5e4907d8987F3fc919BD60351e7a5563]WBNB -- 0.01% [0x47a90A2d92A8367A91EfA1906bFc8c1E05bf10c4]USDT -- 0.05% [0xcCDFcd1aaC447D5B29980f64b831c532a6a33726]USDC, [V4] 5.00% = 4 -- 0.98% [0xfdbc2887ab2cdcdc680775821f00ba90632ae4e9e7a9d3c125d308e0a3338aa8]USDT -- 0.0005% [0xb539a6a4cf8468fec432b99c57dc59049d61ec907c9d6789ec8e34158b214670]USDC",
        "blockNumber": "63970846",
        "quoteId": "c9a21fb7-a826-4bf9-ba9c-ea2e81ad3998",
        "gasPrice": "150000000",
        "txFailureReasons": [],
        "portionBips": 25,
        "portionAmount": "2500000000000000000",
        "portionRecipient": "0x7FFC3DBF3B2b50Ff3A1D5523bc24Bb5043837B14",
        "gasEstimates": [
            {
                "type": "legacy",
                "strategy": {
                    "limitInflationFactor": 1.15,
                    "priceInflationFactor": 1.5,
                    "percentileThresholdFor1559Fee": 75,
                    "minPriorityFeeGwei": 2,
                    "maxPriorityFeeGwei": 9,
                    "baseFeeMultiplier": 1,
                    "baseFeeHistoryWindow": 20,
                    "minPriorityFeeRatioOfBaseFee": 0.2,
                    "thresholdToInflateLastBlockBaseFee": 0.75
                },
                "gasLimit": "541689",
                "gasFee": "81253350000000",
                "gasPrice": "150000000"
            }
        ],
        "aggregatedOutputs": [
            {
                "amount": "1000000000000000000000",
                "token": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
                "recipient": "0xAAAA44272dc658575Ba38f43C438447dDED45358",
                "bps": 9975
            },
            {
                "amount": "2500000000000000000",
                "token": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
                "recipient": "0x7FFC3DBF3B2b50Ff3A1D5523bc24Bb5043837B14",
                "bps": 25
            }
        ]
    }
}