from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import TextSelector, TextSelectorType, TextSelectorConfig

from custom_components.inim_prime.const import (
    CONF_HOST,
    CONF_API_KEY,
    CONF_USE_HTTPS,
    CONF_SERIAL_NUMBER,
    DOMAIN, CONF_PANEL_LOG_EVENTS_FETCH_LIMIT, CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_DEFAULT,
    CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_MIN, CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_MAX,
)
from inim_prime import InimPrimeClient


class InimPrimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for INIM Prime integration."""
    VERSION = 1
    MINOR_VERSION = 0

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step initiated by the user."""
        errors = {}

        if user_input is not None:
            conf_host: str = user_input[CONF_HOST].strip()
            conf_api_key: str = user_input[CONF_API_KEY].strip()
            conf_use_https: bool = user_input.get(CONF_USE_HTTPS, True)
            conf_serial_number: str = user_input[CONF_SERIAL_NUMBER].strip()
            conf_panel_log_events_fetch_limit: int = user_input[CONF_PANEL_LOG_EVENTS_FETCH_LIMIT]

            await self.async_set_unique_id(conf_serial_number)
            self._abort_if_unique_id_configured()

            try:
                client = InimPrimeClient(
                    host=conf_host,
                    api_key=conf_api_key,
                    use_https=conf_use_https,
                )
                await client.connect()
                await client.close()
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"INIM Prime ({conf_serial_number})",
                    data={
                        CONF_HOST: conf_host,
                        CONF_API_KEY: conf_api_key,
                        CONF_SERIAL_NUMBER: conf_serial_number
                    },
                    options={
                        CONF_USE_HTTPS: conf_use_https,
                        CONF_PANEL_LOG_EVENTS_FETCH_LIMIT: conf_panel_log_events_fetch_limit,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_API_KEY): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.PASSWORD)
                ),
                vol.Optional(CONF_USE_HTTPS, default=True): bool,
                vol.Required(CONF_SERIAL_NUMBER): str,
                vol.Required(
                    CONF_PANEL_LOG_EVENTS_FETCH_LIMIT,
                    default=CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_DEFAULT,
                ): vol.All(
                    int,
                    vol.Range(
                        min=CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_MIN,
                        max=CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_MAX,
                    ),
                ),
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @classmethod
    @callback
    def async_get_options_flow(cls, config_entry):
        """Return the options flow handler for this integration."""
        return InimPrimeOptionsFlowHandler()

class InimPrimeOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for the INIM Prime integration."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage options."""
        if user_input:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_USE_HTTPS,
                    default=self.config_entry.data.get(CONF_USE_HTTPS, True),
                ): bool,
                vol.Optional(
                    CONF_PANEL_LOG_EVENTS_FETCH_LIMIT,
                    default=self.config_entry.options.get(
                        CONF_PANEL_LOG_EVENTS_FETCH_LIMIT,
                        CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_DEFAULT
                    ),
                ): vol.All(int, vol.Range(
                    min=CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_MIN,
                    max=CONF_PANEL_LOG_EVENTS_FETCH_LIMIT_MAX,
                )),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)