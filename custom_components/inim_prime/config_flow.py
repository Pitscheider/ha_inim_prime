
import voluptuous as vol
from homeassistant import config_entries

from custom_components.inim_prime.const import CONF_HOST, CONF_API_KEY, CONF_USE_HTTPS, DOMAIN
from inim_prime import InimPrimeClient


class InimPrimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                client = InimPrimeClient(
                    host=user_input[CONF_HOST],
                    api_key=user_input[CONF_API_KEY],
                    use_https=user_input[CONF_USE_HTTPS],
                )
                await client.connect()
                await client.close()

                return self.async_create_entry(
                    title="INIM Prime",
                    data=user_input,
                )
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_USE_HTTPS, default=True): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
