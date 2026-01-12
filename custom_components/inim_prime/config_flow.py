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
    DOMAIN,
)
from inim_prime import InimPrimeClient


class InimPrimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for INIM Prime integration."""
    VERSION = 1  # Major version
    MINOR_VERSION = 0  # Minor version for migration tracking

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step initiated by the user."""
        errors = {}

        if user_input is not None:
            conf_host: str = user_input[CONF_HOST].strip()
            conf_api_key: str = user_input[CONF_API_KEY].strip()
            conf_use_https: bool = user_input.get(CONF_USE_HTTPS, True)
            conf_serial_number: str = user_input[CONF_SERIAL_NUMBER].strip()

            # Ensure unique ID is set to prevent duplicate entries
            await self.async_set_unique_id(conf_serial_number)
            self._abort_if_unique_id_configured()

            # Attempt to connect to the device to verify credentials
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
                # Create the config entry
                return self.async_create_entry(
                    title=f"INIM Prime ({conf_serial_number})",
                    data={
                        CONF_HOST: conf_host,
                        CONF_API_KEY: conf_api_key,
                        CONF_USE_HTTPS: conf_use_https,
                        CONF_SERIAL_NUMBER: conf_serial_number,
                    },
                )

        # Show the form if no input or if there were errors
        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_API_KEY): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
                vol.Optional(CONF_USE_HTTPS, default=True): bool,
                vol.Required(CONF_SERIAL_NUMBER): str,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(self, config_entry) -> config_entries.OptionsFlow:
        """Return the options flow handler for this integration."""
        return InimPrimeOptionsFlowHandler(config_entry)


class InimPrimeOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for the INIM Prime integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_USE_HTTPS,
                    default=self.config_entry.data.get(CONF_USE_HTTPS, True),
                ): bool,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
