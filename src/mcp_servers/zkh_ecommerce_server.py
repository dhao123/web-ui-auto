"""
震坤行电商测试专用MCP服务器
提供价格提取、购物车验证、智能等待、网络捕获等工具
"""
import re
import asyncio
import logging
from typing import Any, Dict, List, Optional
from playwright.async_api import Page, ElementHandle

logger = logging.getLogger(__name__)


class ZKHEcommerceServer:
    """震坤行电商MCP服务器"""
    
    def __init__(self):
        self.name = "zkh-ecommerce"
        self.version = "1.0.0"
        self.description = "震坤行电商测试专用工具集"
    
    async def extract_price(
        self,
        page: Page,
        price_type: str = "untaxed",
        selector: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        提取价格工具
        
        Args:
            page: Playwright页面对象
            price_type: 价格类型 ("untaxed" 未税价, "taxed" 含税价)
            selector: 自定义选择器（可选）
        
        Returns:
            {
                "success": bool,
                "price": float,
                "price_text": str,
                "currency": str,
                "error": str
            }
        """
        try:
            # 定义价格选择器优先级列表
            if price_type == "untaxed":
                selectors = [
                    selector,  # 自定义选择器优先
                    "[class*='untax']",  # 未税价class
                    "[class*='price'][class*='no-tax']",
                    "text=/未税价/",
                    "text=/不含税/",
                    ".price-untaxed",
                    "[data-price-type='untaxed']",
                ]
            else:
                selectors = [
                    selector,
                    "[class*='price']",
                    ".price",
                    "[data-price-type='taxed']",
                ]
            
            # 过滤None值
            selectors = [s for s in selectors if s]
            
            price_text = None
            for sel in selectors:
                try:
                    element = await page.wait_for_selector(sel, timeout=3000)
                    if element:
                        price_text = await element.inner_text()
                        if price_text:
                            break
                except Exception:
                    continue
            
            if not price_text:
                return {
                    "success": False,
                    "price": None,
                    "price_text": None,
                    "currency": "CNY",
                    "error": "未找到价格元素"
                }
            
            # 提取数字（支持格式：¥18.50, 18.50元, 18.50）
            price_match = re.search(r'(\d+\.?\d*)', price_text.replace(',', ''))
            if not price_match:
                return {
                    "success": False,
                    "price": None,
                    "price_text": price_text,
                    "currency": "CNY",
                    "error": f"无法从文本中提取价格: {price_text}"
                }
            
            price = float(price_match.group(1))
            
            logger.info(f"成功提取价格: {price} (原始文本: {price_text})")
            
            return {
                "success": True,
                "price": price,
                "price_text": price_text,
                "currency": "CNY",
                "error": None
            }
            
        except Exception as e:
            logger.error(f"价格提取失败: {e}")
            return {
                "success": False,
                "price": None,
                "price_text": None,
                "currency": "CNY",
                "error": str(e)
            }
    
    async def verify_cart_status(
        self,
        page: Page,
        expected_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        验证购物车状态工具
        
        Args:
            page: Playwright页面对象
            expected_count: 期望的购物车商品数量（可选）
        
        Returns:
            {
                "success": bool,
                "cart_count": int,
                "has_items": bool,
                "message": str,
                "error": str
            }
        """
        try:
            # 定义购物车数量选择器
            cart_selectors = [
                ".cart-count",
                "[class*='cart'][class*='num']",
                "[class*='cart'][class*='count']",
                "[data-cart-count]",
                ".shopping-cart .count",
            ]
            
            cart_count = 0
            cart_text = None
            
            for sel in cart_selectors:
                try:
                    element = await page.wait_for_selector(sel, timeout=2000)
                    if element:
                        cart_text = await element.inner_text()
                        # 提取数字
                        count_match = re.search(r'(\d+)', cart_text)
                        if count_match:
                            cart_count = int(count_match.group(1))
                            break
                except Exception:
                    continue
            
            # 检查是否有"加入购物车成功"提示
            success_indicators = [
                "text=/加入购物车成功/",
                "text=/添加成功/",
                ".success-message",
                "[class*='success'][class*='tip']",
            ]
            
            has_success_message = False
            for sel in success_indicators:
                try:
                    element = await page.query_selector(sel)
                    if element:
                        has_success_message = True
                        break
                except Exception:
                    continue
            
            has_items = cart_count > 0 or has_success_message
            
            # 验证期望数量
            if expected_count is not None:
                count_match = cart_count == expected_count
                message = f"购物车数量: {cart_count}, 期望: {expected_count}, 匹配: {count_match}"
                success = count_match
            else:
                message = f"购物车数量: {cart_count}, 有商品: {has_items}"
                success = has_items
            
            logger.info(message)
            
            return {
                "success": success,
                "cart_count": cart_count,
                "has_items": has_items,
                "has_success_message": has_success_message,
                "message": message,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"购物车状态验证失败: {e}")
            return {
                "success": False,
                "cart_count": 0,
                "has_items": False,
                "has_success_message": False,
                "message": None,
                "error": str(e)
            }
    
    async def wait_for_element(
        self,
        page: Page,
        selector: str,
        timeout: int = 10000,
        state: str = "visible"
    ) -> Dict[str, Any]:
        """
        智能等待元素工具
        
        Args:
            page: Playwright页面对象
            selector: 元素选择器
            timeout: 超时时间（毫秒）
            state: 等待状态 ("visible", "attached", "hidden")
        
        Returns:
            {
                "success": bool,
                "found": bool,
                "selector": str,
                "wait_time": float,
                "error": str
            }
        """
        import time
        start_time = time.time()
        
        try:
            await page.wait_for_selector(
                selector,
                timeout=timeout,
                state=state
            )
            
            wait_time = time.time() - start_time
            
            logger.info(f"元素已出现: {selector}, 等待时间: {wait_time:.2f}s")
            
            return {
                "success": True,
                "found": True,
                "selector": selector,
                "wait_time": round(wait_time, 2),
                "error": None
            }
            
        except Exception as e:
            wait_time = time.time() - start_time
            logger.warning(f"元素等待超时: {selector}, 等待时间: {wait_time:.2f}s")
            
            return {
                "success": False,
                "found": False,
                "selector": selector,
                "wait_time": round(wait_time, 2),
                "error": str(e)
            }
    
    async def capture_network(
        self,
        page: Page,
        url_pattern: Optional[str] = None,
        duration: int = 5000
    ) -> Dict[str, Any]:
        """
        捕获网络请求工具（用于调试）
        
        Args:
            page: Playwright页面对象
            url_pattern: URL匹配模式（正则表达式）
            duration: 捕获时长（毫秒）
        
        Returns:
            {
                "success": bool,
                "requests": List[Dict],
                "count": int,
                "error": str
            }
        """
        try:
            captured_requests = []
            
            def handle_request(request):
                if url_pattern:
                    if re.search(url_pattern, request.url):
                        captured_requests.append({
                            "url": request.url,
                            "method": request.method,
                            "headers": dict(request.headers),
                        })
                else:
                    captured_requests.append({
                        "url": request.url,
                        "method": request.method,
                        "headers": dict(request.headers),
                    })
            
            page.on("request", handle_request)
            
            # 等待指定时长
            await asyncio.sleep(duration / 1000)
            
            page.remove_listener("request", handle_request)
            
            logger.info(f"捕获到 {len(captured_requests)} 个网络请求")
            
            return {
                "success": True,
                "requests": captured_requests,
                "count": len(captured_requests),
                "error": None
            }
            
        except Exception as e:
            logger.error(f"网络请求捕获失败: {e}")
            return {
                "success": False,
                "requests": [],
                "count": 0,
                "error": str(e)
            }


# MCP服务器工具定义（用于注册到Controller）
MCP_TOOLS = {
    "extract_price": {
        "description": "从页面中提取价格（支持未税价和含税价）",
        "parameters": {
            "price_type": {
                "type": "string",
                "description": "价格类型: 'untaxed' (未税价) 或 'taxed' (含税价)",
                "default": "untaxed"
            },
            "selector": {
                "type": "string",
                "description": "自定义CSS选择器（可选）",
                "default": None
            }
        }
    },
    "verify_cart_status": {
        "description": "验证购物车状态和商品数量",
        "parameters": {
            "expected_count": {
                "type": "integer",
                "description": "期望的购物车商品数量（可选）",
                "default": None
            }
        }
    },
    "wait_for_element": {
        "description": "智能等待页面元素出现",
        "parameters": {
            "selector": {
                "type": "string",
                "description": "CSS选择器或文本选择器",
                "required": True
            },
            "timeout": {
                "type": "integer",
                "description": "超时时间（毫秒）",
                "default": 10000
            },
            "state": {
                "type": "string",
                "description": "等待状态: 'visible', 'attached', 'hidden'",
                "default": "visible"
            }
        }
    },
    "capture_network": {
        "description": "捕获网络请求（用于调试和问题定位）",
        "parameters": {
            "url_pattern": {
                "type": "string",
                "description": "URL匹配模式（正则表达式，可选）",
                "default": None
            },
            "duration": {
                "type": "integer",
                "description": "捕获时长（毫秒）",
                "default": 5000
            }
        }
    }
}
