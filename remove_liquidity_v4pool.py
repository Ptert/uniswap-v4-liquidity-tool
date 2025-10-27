# 解析 modifyLiquidities calldata 的辅助工具
from datetime import datetime, timezone
from typing import List, Dict, Any
from web3 import Web3
from eth_abi import decode, encode
import time


def decode_modify_liquidities_from_words(method_selector_hex: str, words_hex: List[str]) -> Dict[str, Any]:
    """将 MethodID + 32字节槽列表组合为 calldata，并解析为结构化结果。
    返回包含 deadline、本地时间、actions、params 的字典。
    """
    # 拼接完整 calldata（4字节方法选择器 + 参数编码）
    calldata_hex = method_selector_hex + ''.join(words_hex)
    calldata_bytes = bytes.fromhex(calldata_hex[2:])

    # 跳过 4 字节选择器，解码函数参数 (bytes unlockData, uint256 deadline)
    args = decode(['bytes', 'uint256'], calldata_bytes[4:])
    unlock_data_bytes, deadline_int = args[0], args[1]

    # 解码 unlockData = abi.encode(bytes actions, bytes[] params)
    actions_bytes, params_bytes_list = decode(['bytes', 'bytes[]'], unlock_data_bytes)
    actions_list = list(actions_bytes)  # 每个字节一个动作编号

    # 将 deadline 转为本地时间
    local_dt = datetime.fromtimestamp(deadline_int, tz=timezone.utc).astimezone()

    # 根据动作编号解析每个 params[i]
    decoded_params: List[Dict[str, Any]] = []
    for idx, action in enumerate(actions_list):
        p_bytes = params_bytes_list[idx]
        if action == 0x01:  # DECREASE_LIQUIDITY
            token_id, liquidity, amount0_min, amount1_min, hook_data = decode(
                ['uint256', 'uint128', 'uint128', 'uint128', 'bytes'], p_bytes
            )
            decoded_params.append({
                'action': 'DECREASE_LIQUIDITY',
                'tokenId': int(token_id),
                'liquidity': int(liquidity),
                'amount0Min': int(amount0_min),
                'amount1Min': int(amount1_min),
                'hookDataHex': '0x' + hook_data.hex(),
            })
        elif action == 0x11:  # TAKE_PAIR（领取两端代币）
            currency0, currency1, recipient = decode(
                ['address', 'address', 'address'], p_bytes
            )
            decoded_params.append({
                'action': 'TAKE_PAIR',
                'currency0': Web3.to_checksum_address(currency0),
                'currency1': Web3.to_checksum_address(currency1),
                'recipient': Web3.to_checksum_address(recipient),
            })
        else:
            decoded_params.append({
                'action': f'UNKNOWN_0x{action:02x}',
                'raw': '0x' + p_bytes.hex(),
            })

    return {
        'deadline': int(deadline_int),
        'deadline_local': local_dt.isoformat(),
        'actions': actions_list,
        'params': decoded_params,
    }


def encode_modify_liquidities_unlock_data(
    token_id: int,
    currency0: str,
    currency1: str,
    recipient: str,
    liquidity: int = 0,
    amount0_min: int = 0,
    amount1_min: int = 0,
    hook_data: bytes = b'',
) -> str:
    """按 v4 PositionManager 的参数约定，编码 unlockData = abi.encode(actions(bytes), params(bytes[]))。
    动作序列为 [0x01 (DECREASE_LIQUIDITY), 0x11 (TAKE_PAIR)]。
    返回 0x 前缀的十六进制字符串。
    """
    # 编码 DECREASE_LIQUIDITY 参数 (uint256 tokenId, uint128 liquidity, uint128 amount0Min, uint128 amount1Min, bytes hookData)
    dec_params = encode(
        ['uint256', 'uint128', 'uint128', 'uint128', 'bytes'],
        [int(token_id), int(liquidity), int(amount0_min), int(amount1_min), hook_data]
    )

    # 编码 TAKE_PAIR 参数 (address currency0, address currency1, address recipient)
    take_params = encode(
        ['address', 'address', 'address'],
        [Web3.to_checksum_address(currency0), Web3.to_checksum_address(currency1), Web3.to_checksum_address(recipient)]
    )

    actions_bytes = bytes([0x01, 0x11])
    unlock_data_bytes = encode(['bytes', 'bytes[]'], [actions_bytes, [dec_params, take_params]])
    return '0x' + unlock_data_bytes.hex()
if __name__ == '__main__':
    # ---- 根据你的参数生成 unlockData 与 deadline ----
    USER_TOKEN_ID = 60375
    CURRENCY0 = '0x55d398326f99059fF775485246999027B3197955'
    CURRENCY1 = '0xfAB99fCF605fD8f4593EDb70A43bA56542777777'
    RECIPIENT = '0xD290A5E8b8f4fB82B22104C7543574CCd48ab472'
    LIQUIDITY = 2069679014400569651           # 若要撤出本金，请改为你的实际数值（uint128）
    AMOUNT0_MIN = 0         # 为避免滑点，可以设为你期望的最小值
    AMOUNT1_MIN = 0
    HOOK_DATA = b''         # 如无 Hook，保持空字节

    unlock_hex = encode_modify_liquidities_unlock_data(
        USER_TOKEN_ID, CURRENCY0, CURRENCY1, RECIPIENT,
        LIQUIDITY, AMOUNT0_MIN, AMOUNT1_MIN, HOOK_DATA
    )
    print('unlockData (bytes hex):', unlock_hex)
    deadline_int = int(time.time() + 1200)
    print('deadline (uint256):', deadline_int)


