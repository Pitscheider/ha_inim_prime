
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components import serial

from custom_components.inim_prime.const import CONF_HOST, CONF_API_KEY, CONF_USE_HTTPS, DOMAIN, CONF_SERIAL_NUMBER
from inim_prime import InimPrimeClient


class InimPrimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                conf_host: str = user_input[CONF_HOST].strip()
                conf_api_key: str = user_input[CONF_API_KEY].strip()
                conf_use_https: bool = user_input[CONF_USE_HTTPS]
                conf_serial_number: str = user_input[CONF_SERIAL_NUMBER].strip()

                await self.async_set_unique_id(conf_serial_number)
                self._abort_if_unique_id_configured()

                client = InimPrimeClient(
                    host = conf_host,
                    api_key = conf_api_key,
                    use_https = conf_use_https,
                )

                await client.connect()
                await client.close()

                return self.async_create_entry(
                    title=f"INIM Prime ({conf_serial_number}",
                    data = {
                        CONF_HOST: conf_host,
                        CONF_API_KEY: conf_api_key,
                        CONF_USE_HTTPS: conf_use_https,
                        CONF_SERIAL_NUMBER: conf_serial_number,
                    },
                )
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_USE_HTTPS, default=True): bool,
                vol.Required(CONF_SERIAL_NUMBER): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
