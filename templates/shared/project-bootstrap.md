# Project Bootstrap Template

## 1. Initialize WordPress Plugin Project

### 1.1 Directory Structure
```bash
# Create project structure
mkdir -p [plugin-name]/{src/Core/{Module/{Handler,Service,Shortcodes},Shared},views/module/{_partials},assets/{scss,js,dist},tests/{unit,integration,features}}
```

### 1.2 Main Plugin File ([plugin-name].php)
```php
<?php
/**
 * Plugin Name: [Plugin Name]
 * Plugin URI: https://example.com/[plugin-name]
 * Description: [Plugin description]
 * Version: 1.0.0
 * Author: [Author Name]
 * Author URI: https://example.com
 * License: GPL-2.0-or-later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: [text-domain]
 * Requires at least: 5.0
 * Requires PHP: 8.0
 * Tested up to: 6.5
 */

if (!defined('ABSPATH')) {
    exit;
}

// Define constants
define('PLUGIN_DIR', plugin_dir_path(__FILE__));
define('PLUGIN_URL', plugin_dir_url(__FILE__));
define('PLUGIN_VERSION', '1.0.0');
define('PLUGIN_TEXT_DOMAIN', '[text-domain]');

// Autoloader
spl_autoload_register(function ($class) {
    $prefix = '[Namespace]\\';
    $base_dir = PLUGIN_DIR . 'src/Core/';
    
    $len = strlen($prefix);
    if (strncmp($prefix, $class, $len) !== 0) {
        return;
    }
    
    $relative_class = substr($class, $len);
    $file = $base_dir . str_replace('\\', '/', $relative_class) . '.php';
    
    if (file_exists($file)) {
        require $file;
    }
});

// Activation/Deactivation hooks
register_activation_hook(__FILE__, '[namespace]_activate');
register_deactivation_hook(__FILE__, '[namespace]_deactivate');

// Bootstrap
function [namespace]_init() {
    load_plugin_textdomain('[text-domain]', false, dirname(plugin_basename(__FILE__)) . '/languages');
    
    $plugin = new \[Namespace]\Plugin();
    $plugin->init();
}
add_action('plugins_loaded', '[namespace]_init');

function [namespace]_activate() {
    // Create custom tables if needed
    // Set default options
    flush_rewrite_rules();
}

function [namespace]_deactivate() {
    // Clean up cron schedules
    flush_rewrite_rules();
}
```

### 1.3 Plugin Class (src/Core/Plugin.php)
```php
<?php
namespace [Namespace];

class Plugin {
    private static ?self $instance = null;
    
    public static function instance(): self {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function __construct() {}
    private function __clone() {}
    private function __wakeup() {}
    
    public function init(): void {
        $this->register_hooks();
        $this->register_ajax_handlers();
    }
    
    private function register_hooks(): void {
        // Register shortcodes
        add_action('init', [$this, 'register_shortcodes']);
    }
    
    public function register_shortcodes(): void {
        // Example: $shortcode = new \[Namespace]\Shortcodes\Product\ProductListShortcode($this);
        // $shortcode->register();
    }
    
    private function register_ajax_handlers(): void {
        // add_action('wp_ajax_[module-prefix]_action', [$this, 'handle_[module-prefix]_action']);
        // add_action('wp_ajax_nopriv_[module-prefix]_action', [$this, 'handle_[module-prefix]_action']);
    }
}
```

### 1.4 Base Classes

**src/Core/Shared/BaseShortcode.php:**
```php
<?php
namespace [Namespace]\Shared;

abstract class BaseShortcode {
    protected $plugin;
    private const STYLE = '[module-prefix]-style';
    private const SCRIPT = '[module-prefix]-script';
    
    public function __construct($plugin) {
        $this->plugin = $plugin;
        $this->register_assets();
    }
    
    abstract public function register_assets();
    
    public function register(): void {
        add_shortcode($this->get_shortcode_tag(), [$this, 'render']);
    }
    
    abstract public function get_shortcode_tag(): string;
    
    public function render($atts, $content = null, $shortcode_name = '') {
        $vars = $this->prepare_vars($atts, $content, $shortcode_name);
        return $this->render_view('index.php', $vars);
    }
    
    protected function render_view($template, $vars): string {
        extract($vars);
        ob_start();
        require PLUGIN_DIR . "views/{$template}";
        return ob_get_clean();
    }
    
    protected function prepare_vars($atts, $content, $shortcode_name): array {
        return [
            'data' => [],
            'nonce' => wp_create_nonce('[module-prefix]_' . $shortcode_name),
            'plugin_url' => PLUGIN_URL,
        ];
    }
}
```

**src/Core/Shared/BaseHandler.php:**
```php
<?php
namespace [Namespace]\Shared;

abstract class BaseHandler {
    protected $plugin;
    
    public function __construct($plugin) {
        $this->plugin = $plugin;
    }
    
    protected function get_option(string $key, $default = null) {
        return get_option('[namespace]_settings', [])[$key] ?? $default;
    }
    
    protected function nonce_check(string $action): bool {
        return isset($_POST['nonce']) && wp_verify_nonce($_POST['nonce'], $action);
    }
    
    protected function check_capability(string $capability): bool {
        return current_user_can($capability);
    }
    
    protected function send_json_success($data = []): void {
        wp_send_json_success($data);
    }
    
    protected function send_json_error(string $message = '', int $status = 400): void {
        wp_send_json_error(['message' => $message], $status);
    }
}
```

## 2. Asset Build Setup

### 2.1 package.json
```json
{
    "name": "[plugin-name]",
    "version": "1.0.0",
    "scripts": {
        "build:scss": "node-sass assets/scss/ -o assets/dist/css/ --source-map true",
        "build:js": "webpack --mode production",
        "watch:scss": "node-sass assets/scss/ -o assets/dist/css/ --watch",
        "watch:js": "webpack --mode development --watch",
        "build": "npm run build:scss && npm run build:js",
        "watch": "npm run watch:scss & npm run watch:js"
    },
    "devDependencies": {
        "node-sass": "^9.0.0",
        "webpack": "^5.88.0",
        "webpack-cli": "^5.1.0"
    }
}
```

### 2.2 SCSS Entry (assets/scss/main.scss)
```scss
// Custom properties
:root {
    --[module-prefix]-spacing-sm: 8px;
    --[module-prefix]-spacing-md: 16px;
    --[module-prefix]-spacing-lg: 24px;
    --[module-prefix]-color-primary: #0073aa;
    --[module-prefix]-color-text: #333;
    --[module-prefix]-color-border: #ddd;
}

@import "variables";
@import "mixins";
@import "product-list";
@import "product-card";
```

### 2.3 JS Entry (assets/js/main.js)
```javascript
(function($) {
    'use strict';
    
    var self = {
        init: function() {
            this.cache_dom();
            this.bind_events();
            this.render();
        },
        
        cache_dom: function() {
            this.$container = $('.[module-prefix]');
        },
        
        bind_events: function() {
            // Event bindings here
        },
        
        render: function() {
            // Initial render
        }
    };
    
    $(document).ready(function() {
        self.init();
    });
    
    $.[moduleNamespace] = self;
})(jQuery);
```

## 3. Testing Setup

### 3.1 composer.json (testing)
```json
{
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "yoast/phpunit-polyfills": "^2.0",
        "php-parallel-lint/php-parallel-lint": "^1.3",
        "phpcompatibility/phpcompatibility-wp": "^2.1"
    },
    "scripts": {
        "phpunit": "vendor/bin/phpunit",
        "lint": "vendor/bin/parallel-lint --exclude vendor --exclude node_modules .",
        "phpcs": "vendor/bin/phpcs --standard=WordPress"
    }
}
```

### 3.2 phpunit.xml.dist
```xml
<?xml version="1.0"?>
<phpunit
    bootstrap="tests/bootstrap.php"
    backupGlobals="false"
    colors="true"
>
    <testsuites>
        <testsuite name="[Plugin_Name] Tests">
            <directory suffix="Test.php">./tests/unit</directory>
            <directory suffix="Test.php">./tests/integration</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

### 3.3 tests/bootstrap.php
```php
<?php
$_tests_dir = getenv('WP_TESTS_DIR');
if (!$_tests_dir) {
    $_tests_dir = '/tmp/wordpress-tests-lib';
}

require_once $_tests_dir . '/includes/functions.php';

tests_add_filter('muplugins_loaded', function() {
    require_once __DIR__ . '/../../src/Core/Plugin.php';
});

tests_add_filter('muplugins_loaded', function() {
    // Load plugin
    require_once __DIR__ . '/../../[plugin-name].php';
});

function _manually_load_plugin() {
    require_once __DIR__ . '/../../[plugin-name].php';
}
tests_add_filter('plugins_loaded', '_manually_load_plugin');

define('PLUGIN_DIR', __DIR__ . '/../');

tests_add_filter('setup_theme', function() {
    // Set up test environment
});
```

## 4. .gitignore

```
# Dependencies
vendor/
node_modules/

# Build artifacts
assets/dist/
build/
dist/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
error_log

# Env
.env
.env.local

# AI generated
.ai-cache/
.generated/
```

## 5. .editorconfig

```
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.php]
indent_style = space
indent_size = 4

[*.js]
indent_style = space
indent_size = 4

[*.scss]
indent_style = space
indent_size = 4

[*.json]
indent_style = space
indent_size = 4
```

## 6. README.md Template

```markdown
# [Plugin Name]

[Plugin description]

## Requirements

- WordPress 5.0+
- PHP 8.0+

## Installation

1. Upload the plugin folder to `/wp-content/plugins/`
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Go to Settings → [Plugin Name] to configure

## Usage

Use the shortcode in your posts/pages:

```
[module-prefix] category="cat-1" limit="10"
```

## Changelog

### 1.0.0
- Initial release

## License

GPL-2.0-or-later
```

## 7. Project Context (.ai/context.yaml)

```yaml
name: [plugin-name]
stack:
  - wordpress
  - php-8.0
  - jquery
  - node-sass

modules:
  - product
  - event
  - shortcode

rules:
  namespace: "[Namespace]\\[Module]\\[SubModule]"
  meta_prefix: "[namespace]_"
  text_domain: "[text-domain]"
  coding_standard: "PSR-12"
  php_version: "8.0"
```

## 8. Quick Start Commands

```bash
# Clone and setup
git clone <repo-url>
cd [plugin-name]
npm install
composer install --dev

# Build assets
npm run build

# Watch for changes
npm run watch

# Run tests
./vendor/bin/phpunit

# Lint PHP
./vendor/bin/parallel-lint --exclude vendor --exclude node_modules .

# Start development
# 1. Add to wp-content/plugins/
# 2. Activate in WordPress admin
# 3. Run npm run watch
```

## 9. File Checklist

After bootstrapping, verify:

- [ ] `[plugin-name].php` exists with proper header
- [ ] `src/Core/Plugin.php` singleton class
- [ ] `src/Core/Shared/BaseShortcode.php`
- [ ] `src/Core/Shared/BaseHandler.php`
- [ ] `views/` directory structure
- [ ] `assets/scss/` entry file
- [ ] `assets/js/` entry file
- [ ] `tests/` directory with bootstrap
- [ ] `phpunit.xml.dist`
- [ ] `package.json` with scripts
- [ ] `.gitignore`
- [ ] `.editorconfig`
- [ ] `README.md`
- [ ] `languages/` directory for translations
