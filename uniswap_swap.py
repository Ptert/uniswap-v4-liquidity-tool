from typing import Optional, Tuple, Dict, Any
import math
import time
from dataclasses import dataclass

from web3 import Web3
from web3.contract import Contract
from eth_account import Account


@dataclass
class TxResult:
    success: bool
    tx_hash: Optional[str] = None
    error: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None


class PancakeV3Liquidity:
    """
    使用 Python 在 BSC 主网进行 PancakeSwap v3（Uniswap v3 fork）添加/移除流动性。
    说明：PancakeSwap v3 的流动性头寸使用 NonfungiblePositionManager 管理，与 Uniswap v3 接口一致。
    """

    # BSC 主网合约地址（官方文档）
    ADDRS = {
        "Factory": Web3.to_checksum_address("0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865"),
        "NonfungiblePositionManager": Web3.to_checksum_address("0x46A15B0b27311cedF172AB29E4f4766fbE7F4364"),
        "SwapRouterV3": Web3.to_checksum_address("0x1b81D678ffb9C0263b24A97847620C99d213eB14"),
        "SmartRouter": Web3.to_checksum_address("0x13f4EA83D0bd40E75C8222255bc855a974568Dd4"),
    }

    # 最小 ABI 片段
    ABIS = {
        "ERC20": [
            {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
             "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
             "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
             "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "spender", "type": "address"},
                         {"internalType": "uint256", "name": "amount", "type": "uint256"}],
             "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
             "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "owner", "type": "address"},
                         {"internalType": "address", "name": "spender", "type": "address"}],
             "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
             "stateMutability": "view", "type": "function"},
        ],
        "Factory": [
            {"inputs": [{"internalType": "address", "name": "token0", "type": "address"},
                         {"internalType": "address", "name": "token1", "type": "address"},
                         {"internalType": "uint24", "name": "fee", "type": "uint24"}],
             "name": "getPool", "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
             "stateMutability": "view", "type": "function"},
        ],
        "Pool": [
            {"inputs": [], "name": "slot0",
             "outputs": [
                 {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
                 {"internalType": "int24", "name": "tick", "type": "int24"},
                 {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
                 {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
                 {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
                 {"internalType": "bool", "name": "feeProtocol", "type": "bool"},
                 {"internalType": "bool", "name": "unlocked", "type": "bool"}
             ], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "tickSpacing",
             "outputs": [{"internalType": "int24", "name": "", "type": "int24"}],
             "stateMutability": "view", "type": "function"},
        ],
        "NonfungiblePositionManager": [
            {"inputs": [{"components": [
                {"internalType": "address", "name": "token0", "type": "address"},
                {"internalType": "address", "name": "token1", "type": "address"},
                {"internalType": "uint24", "name": "fee", "type": "uint24"},
                {"internalType": "int24", "name": "tickLower", "type": "int24"},
                {"internalType": "int24", "name": "tickUpper", "type": "int24"},
                {"internalType": "uint256", "name": "amount0Desired", "type": "uint256"},
                {"internalType": "uint256", "name": "amount1Desired", "type": "uint256"},
                {"internalType": "uint256", "name": "amount0Min", "type": "uint256"},
                {"internalType": "uint256", "name": "amount1Min", "type": "uint256"},
                {"internalType": "address", "name": "recipient", "type": "address"},
                {"internalType": "uint256", "name": "deadline", "type": "uint256"}
            ], "internalType": "struct INonfungiblePositionManager.MintParams", "name": "params", "type": "tuple"}],
             "name": "mint", "outputs": [
                {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                {"internalType": "uint128", "name": "liquidity", "type": "uint128"},
                {"internalType": "uint256", "name": "amount0", "type": "uint256"},
                {"internalType": "uint256", "name": "amount1", "type": "uint256"}
             ], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"components": [
                {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                {"internalType": "uint128", "name": "liquidity", "type": "uint128"},
                {"internalType": "uint256", "name": "amount0Min", "type": "uint256"},
                {"internalType": "uint256", "name": "amount1Min", "type": "uint256"},
                {"internalType": "uint256", "name": "deadline", "type": "uint256"}
            ], "internalType": "struct INonfungiblePositionManager.DecreaseLiquidityParams", "name": "params", "type": "tuple"}],
             "name": "decreaseLiquidity", "outputs": [{"internalType": "uint256", "name": "amount0", "type": "uint256"},
                                                         {"internalType": "uint256", "name": "amount1", "type": "uint256"}],
             "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"components": [
                {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                {"internalType": "address", "name": "recipient", "type": "address"},
                {"internalType": "uint128", "name": "amount0Max", "type": "uint128"},
                {"internalType": "uint128", "name": "amount1Max", "type": "uint128"}
            ], "internalType": "struct INonfungiblePositionManager.CollectParams", "name": "params", "type": "tuple"}],
             "name": "collect", "outputs": [
                {"internalType": "uint256", "name": "amount0", "type": "uint256"},
                {"internalType": "uint256", "name": "amount1", "type": "uint256"}
             ], "stateMutability": "payable", "type": "function"},
            {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
             "name": "burn", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
             "name": "positions", "outputs": [
                {"internalType": "uint96", "name": "nonce", "type": "uint96"},
                {"internalType": "address", "name": "operator", "type": "address"},
                {"internalType": "address", "name": "token0", "type": "address"},
                {"internalType": "address", "name": "token1", "type": "address"},
                {"internalType": "uint24", "name": "fee", "type": "uint24"},
                {"internalType": "int24", "name": "tickLower", "type": "int24"},
                {"internalType": "int24", "name": "tickUpper", "type": "int24"},
                {"internalType": "uint128", "name": "liquidity", "type": "uint128"},
                {"internalType": "uint256", "name": "feeGrowthInside0LastX128", "type": "uint256"},
                {"internalType": "uint256", "name": "feeGrowthInside1LastX128", "type": "uint256"},
                {"internalType": "uint128", "name": "tokensOwed0", "type": "uint128"},
                {"internalType": "uint128", "name": "tokensOwed1", "type": "uint128"}
             ], "stateMutability": "view", "type": "function"},
        ],
    }

    def __init__(self, w3: Web3, private_key: str):
        self.w3 = w3
        self.private_key = private_key
        self.account: Account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address

    # ---------- 基础工具 ----------
    def _contract(self, address: str, abi_name: str) -> Contract:
        return self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=self.ABIS[abi_name])

    def _send(self, tx: Dict[str, Any]) -> TxResult:
        try:
            tx.setdefault("from", self.address)
            tx.setdefault("nonce", self.w3.eth.get_transaction_count(self.address))
            tx.setdefault("chainId", self.w3.eth.chain_id)
            tx.setdefault("gasPrice", self.w3.eth.gas_price)
            # 估算 gas
            try:
                tx["gas"] = tx.get("gas", self.w3.eth.estimate_gas({k: v for k, v in tx.items() if k != "gas"}))
            except Exception:
                tx["gas"] = tx.get("gas", 800000)
            signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            return TxResult(success=True, tx_hash=self.w3.to_hex(tx_hash))
        except Exception as e:
            return TxResult(success=False, error=str(e))

    def _erc20(self, token: str) -> Contract:
        return self._contract(token, "ERC20")

    def token_decimals(self, token: str) -> int:
        return int(self._erc20(token).functions.decimals().call())

    def token_balance(self, token: str, owner: Optional[str] = None) -> int:
        owner = owner or self.address
        return int(self._erc20(token).functions.balanceOf(Web3.to_checksum_address(owner)).call())

    def approve_token(self, token: str, spender: str, amount: int) -> TxResult:
        contract = self._erc20(token)
        tx = contract.functions.approve(Web3.to_checksum_address(spender), int(amount)).build_transaction({
            "from": self.address,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "chainId": self.w3.eth.chain_id,
            "gasPrice": self.w3.eth.gas_price,
        })
        return self._send(tx)

    # ---------- 池子与价格 ----------
    def get_pool(self, tokenA: str, tokenB: str, fee: int) -> str:
        token0, token1 = self.sort_tokens(tokenA, tokenB)
        factory = self._contract(self.ADDRS["Factory"], "Factory")
        pool = factory.functions.getPool(token0, token1, fee).call()
        if int(pool, 16) == 0:
            raise ValueError("指定代币与费率下的池子不存在，无法添加流动性")
        return Web3.to_checksum_address(pool)

    def get_pool_state(self, pool_addr: str) -> Tuple[int, int, int]:
        pool = self._contract(pool_addr, "Pool")
        slot = pool.functions.slot0().call()
        sqrt_price_x96 = int(slot[0])
        tick = int(slot[1])
        tick_spacing = int(pool.functions.tickSpacing().call())
        return sqrt_price_x96, tick, tick_spacing

    @staticmethod
    def sort_tokens(tokenA: str, tokenB: str) -> Tuple[str, str]:
        a = Web3.to_checksum_address(tokenA)
        b = Web3.to_checksum_address(tokenB)
        return (a, b) if a.lower() < b.lower() else (b, a)

    @staticmethod
    def _align_to_spacing(tick: int, spacing: int) -> int:
        # 向下对齐到 spacing 的倍数
        rem = tick % spacing
        return tick - rem

    def compute_ticks_by_percentage(self, sqrt_price_x96: int, tick: int, tick_spacing: int,
                                    pct: float, dec0: int, dec1: int, token0: str, token1: str) -> Tuple[int, int]:
        # 当前价格（token1 / token0），考虑小数位
        ratio = (sqrt_price_x96 / (2 ** 96)) ** 2
        # 调整小数位到“实际价格”
        price = ratio * (10 ** dec0) / (10 ** dec1)
        lower_price = price * (1 - pct)
        upper_price = price * (1 + pct)
        # 将价格转换为 tick：tick = log_{1.0001}(price_adj)
        # price_adj 需要是 token1/token0 的价格（已考虑 decimals）
        def price_to_tick(p: float) -> int:
            return int(math.log(p, 1.0001))

        t_lower = price_to_tick(lower_price)
        t_upper = price_to_tick(upper_price)
        # 保证顺序并对齐到 tickSpacing
        t_lower, t_upper = min(t_lower, t_upper), max(t_lower, t_upper)
        t_lower = self._align_to_spacing(t_lower, tick_spacing)
        t_upper = self._align_to_spacing(t_upper, tick_spacing) + tick_spacing  # 上边界向上扩一档
        # 确保包含当前 tick
        if not (t_lower < tick < t_upper):
            center = self._align_to_spacing(tick, tick_spacing)
            width = max(tick_spacing * 10, abs(t_upper - t_lower))
            t_lower = center - width
            t_upper = center + width
        return int(t_lower), int(t_upper)

    # ---------- 添加流动性 ----------
    def add_liquidity(self,
                      tokenA: str,
                      tokenB: str,
                      fee: int,
                      amountA: float,
                      amountB: float,
                      price_range_pct: float = 0.05,
                      slippage: float = 0.01,
                      recipient: Optional[str] = None,
                      deadline_seconds: int = 900) -> TxResult:
        try:
            recipient = Web3.to_checksum_address(recipient or self.address)
            token0, token1 = self.sort_tokens(tokenA, tokenB)
            dec0, dec1 = self.token_decimals(token0), self.token_decimals(token1)
            amt0 = int(amountA * (10 ** dec0)) if Web3.to_checksum_address(tokenA) == token0 else int(amountB * (10 ** dec0))
            amt1 = int(amountB * (10 ** dec1)) if Web3.to_checksum_address(tokenB) == token1 else int(amountA * (10 ** dec1))

            pool_addr = self.get_pool(token0, token1, fee)
            sqrt_price_x96, cur_tick, tick_spacing = self.get_pool_state(pool_addr)
            tick_lower, tick_upper = self.compute_ticks_by_percentage(sqrt_price_x96, cur_tick, tick_spacing,
                                                                      price_range_pct, dec0, dec1, token0, token1)

            # 授权
            appr0 = self.approve_token(token0, self.ADDRS["NonfungiblePositionManager"], amt0)
            if not appr0.success:
                return appr0
            appr1 = self.approve_token(token1, self.ADDRS["NonfungiblePositionManager"], amt1)
            if not appr1.success:
                return appr1

            pos_mgr = self._contract(self.ADDRS["NonfungiblePositionManager"], "NonfungiblePositionManager")
            amount0_min = int(amt0 * (1 - slippage))
            amount1_min = int(amt1 * (1 - slippage))
            params = (
                token0,
                token1,
                int(fee),
                int(tick_lower),
                int(tick_upper),
                int(amt0),
                int(amt1),
                int(amount0_min),
                int(amount1_min),
                recipient,
                int(time.time()) + deadline_seconds,
            )
            tx = pos_mgr.functions.mint(params).build_transaction({
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "chainId": self.w3.eth.chain_id,
                "gasPrice": self.w3.eth.gas_price,
            })
            sent = self._send(tx)
            if not sent.success:
                return sent
            return TxResult(success=True, tx_hash=sent.tx_hash, extra={
                "pool": pool_addr,
                "tick": cur_tick,
                "tickLower": tick_lower,
                "tickUpper": tick_upper,
                "amount0Desired": amt0,
                "amount1Desired": amt1,
            })
        except Exception as e:
            return TxResult(success=False, error=str(e))

    # ---------- 移除流动性 ----------
    def remove_liquidity(self,
                         token_id: int,
                         percentage: float = 1.0,
                         recipient: Optional[str] = None,
                         burn_nft: bool = True,
                         deadline_seconds: int = 900) -> TxResult:
        try:
            recipient = Web3.to_checksum_address(recipient or self.address)
            pos_mgr = self._contract(self.ADDRS["NonfungiblePositionManager"], "NonfungiblePositionManager")
            pos = pos_mgr.functions.positions(int(token_id)).call()
            liquidity = int(pos[7])
            if liquidity == 0:
                return TxResult(success=False, error="该头寸没有可用的流动性")
            liq_to_decrease = int(liquidity * percentage)
            # 1) decreaseLiquidity
            dec_params = (
                int(token_id),
                int(liq_to_decrease),
                0,  # amount0Min（如需安全可设置最小值）
                0,  # amount1Min
                int(time.time()) + deadline_seconds,
            )
            tx1 = pos_mgr.functions.decreaseLiquidity(dec_params).build_transaction({
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "chainId": self.w3.eth.chain_id,
                "gasPrice": self.w3.eth.gas_price,
            })
            r1 = self._send(tx1)
            if not r1.success:
                return r1
            # 2) collect（收集本金和手续费）
            collect_params = (
                int(token_id),
                recipient,
                (1 << 128) - 1,
                (1 << 128) - 1,
            )
            tx2 = pos_mgr.functions.collect(collect_params).build_transaction({
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "chainId": self.w3.eth.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "value": 0,
            })
            r2 = self._send(tx2)
            if not r2.success:
                return r2
            # 3) burn NFT（可选）
            if burn_nft:
                tx3 = pos_mgr.functions.burn(int(token_id)).build_transaction({
                    "from": self.address,
                    "nonce": self.w3.eth.get_transaction_count(self.address),
                    "chainId": self.w3.eth.chain_id,
                    "gasPrice": self.w3.eth.gas_price,
                })
                r3 = self._send(tx3)
                if not r3.success:
                    return r3
                return TxResult(success=True, tx_hash=r3.tx_hash, extra={"decrease_tx": r1.tx_hash, "collect_tx": r2.tx_hash})
            return TxResult(success=True, tx_hash=r2.tx_hash, extra={"decrease_tx": r1.tx_hash})
        except Exception as e:
            return TxResult(success=False, error=str(e))


# 简易使用示例（请在实际使用时替换为您自己的 RPC 与私钥/地址）
# from web3 import Web3
# w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))
# private_key = "YOUR_PRIVATE_KEY"
# liq = PancakeV3Liquidity(w3, private_key)
#
# # 添加流动性示例：WBNB/USDT，费率 0.25%（2500），价格范围 ±5%
# WBNB = Web3.to_checksum_address("0xBB4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")
# USDT = Web3.to_checksum_address("0x55d398326f99059fF775485246999027B3197955")
# result = liq.add_liquidity(WBNB, USDT, fee=2500, amountA=0.1, amountB=30, price_range_pct=0.05, slippage=0.01)
# print(result)
#
# # 移除流动性示例：将 100% 流动性移除并收集
# remove_res = liq.remove_liquidity(token_id=12345, percentage=1.0, burn_nft=True)
# print(remove_res)