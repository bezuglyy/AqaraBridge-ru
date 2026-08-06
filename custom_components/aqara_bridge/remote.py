"""Aqara Bridge remote"""

import asyncio
import logging
import time
import voluptuous as vol
from datetime import datetime
from homeassistant.helpers import config_validation as cv
from homeassistant.components.remote import (
    ATTR_DELAY_SECS,
    ATTR_NUM_REPEATS,
    DEFAULT_DELAY_SECS,
    RemoteEntity,
    RemoteEntityFeature,
)
from homeassistant.const import CONF_TIMEOUT

from .core.aiot_manager import AiotManager, AiotEntityBase
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER

_LOGGER = logging.getLogger(__name__)

TYPE = "remote"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "pair": AiotRemotePair,
        "ir": AiotRemoteIrda,
        "ir_tv": AiotIRTVEntity,
        "default": AiotRemoteEntity,
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotRemoteEntity(AiotEntityBase, RemoteEntity):
    def __init__(self, hass, device, res_params, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, **kwargs)
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        await self.async_set_resource("remote", True)

    async def async_turn_off(self, **kwargs):
        await self.async_set_resource("remote", False)

    def convert_attr_to_res(self, res_name, attr_value):
        return super().convert_attr_to_res(res_name, attr_value)

    def convert_res_to_attr(self, res_name, res_value):
        return super().convert_res_to_attr(res_name, res_value)


class AiotRemotePair(AiotEntityBase, RemoteEntity):
    def __init__(self, hass, device, res_params, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, **kwargs)
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        await self.async_device_connection(True)

    async def async_turn_off(self, **kwargs):
        await self.async_device_connection(False)


class AiotRemoteIrda(AiotEntityBase, RemoteEntity):
    def __init__(self, hass, device, res_params, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, **kwargs)
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        """Turn the remote on."""

    async def async_turn_off(self, **kwargs):
        """Turn the remote off."""

    async def async_send_command(self, command, **kwargs):
        """send command"""
        num_repeats = kwargs.get(ATTR_NUM_REPEATS, 1)
        delay = kwargs.get(ATTR_DELAY_SECS, DEFAULT_DELAY_SECS)

        for _ in range(num_repeats):
            await self.async_set_resource("irda", command)
            time.sleep(delay)

    async def async_learn_command(self, **kwargs):
        """Handle a learn command."""
        timeout = kwargs.get(CONF_TIMEOUT, 10)

        resp = await self.async_infrared_learn(True, 20)
        if isinstance(resp, dict):
            keyid = resp["keyId"]

            start_time = datetime.utcnow()
            while (datetime.utcnow() - start_time) < datetime.timedelta(
                seconds=timeout
            ):
                message = await self.hass.async_add_executor_job(
                    self.async_received_learnresult, keyid
                )
                # _LOGGER.info("Message received from device: '%s'", message)

                if isinstance(message, dict):
                    log_msg = "Received command is: {}".format(message["ircode"])
                    self.hass.components.persistent_notification.async_create(
                        log_msg, title="Aqara Remote"
                    )
                    return

                if message is None:
                    await self.async_infrared_learn(False)

                await asyncio.sleep(1)


class AiotIRTVEntity(AiotEntityBase, RemoteEntity):
    """Aqara IR TV (virtual.ir_local.tv) via M3 hub cloud IR."""

    def __init__(self, hass, device, res_params, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, **kwargs)
        self._attr_is_on = False
        self._command_map = {}
        self._attr_supported_features = RemoteEntityFeature.LEARN_COMMAND

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        try:
            keys = await self._aiot_manager.session.async_query_ir_keys(self.device.did)
            if isinstance(keys, dict) and "keys" in keys:
                self._command_map = {
                    (k.get("keyName") or "").lower(): k.get("keyId")
                    for k in keys["keys"]
                }
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning("IR TV keys query failed: %s", err)

    async def async_update(self):
        return None

    async def async_fetch_res_values(self, *args):
        return None

    async def async_send_command(self, command, **kwargs):
        for cmd in command:
            key_id = self._command_map.get(str(cmd).lower())
            if key_id is None:
                key_id = str(cmd)
            await self._aiot_manager.session.async_write_ir_click(
                self.device.did, None, key_id=key_id
            )
            await asyncio.sleep(0.1)
