import sys
from app import create_app
from config import Config, PostgresConfig, TestConfig

config_map = {
    'config.Config': Config,
    'config.PostgresConfig': PostgresConfig,
    'config.TestConfig': TestConfig
}

# Default to 'config.Config' if no configuration is provided
config_name = 'config.Config'
if len(sys.argv) > 1:
    config_name = sys.argv[1]

config_class = config_map.get(config_name, Config)

app = create_app(config_class)

if __name__ == '__main__':
    app.run(debug=(config_class == Config))
