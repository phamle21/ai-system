# WordPress Coding Standards

## 1. PHP Standards

### 1.1 PSR-12 Compliance
- [x] Opening brace for classes/methods on same line
- [x] Control structures: space after keyword, brace on same line
- [x] Each statement on its own line
- [x] 4-space indentation (no tabs)
- [x] Line length: soft limit 120 characters

### 1.2 Naming Conventions
```
Type          | Pattern           | Example
--------------|-------------------|---------------------------
Class         | PascalCase        | Handler
Method        | camelCase         | get_user_list()
Function      | snake_case        | is_active()
Constant      | UPPER_SNAKE_CASE  | PLUGIN_VERSION
Variable      | camelCase         | $userName
Interface     | PascalCase + ...  | Cache_Interface
Trait         | PascalCase + ...  | Timestamp_Trait
```

### 1.3 Type Declarations
```php
// PHP 8.0+ typed properties and parameters
class Plugin {
    private string $version;
    private array $settings;
    
    public function handle_request(string $action, int $post_id = 0): bool {
        return true;
    }
}

// Nullable types
public function get_item(?int $id): ?Item_Model {
    return null;
}
```

### 1.4 Error Handling
```php
// Use exceptions for error conditions
throw new \RuntimeException("Item not found: {$id}");

// Catch specific exceptions
try {
    $data = $handler->fetch_data();
} catch (\InvalidArgumentException $e) {
    error_log("Invalid argument: " . $e->getMessage());
    return false;
} catch (\Exception $e) {
    error_log("Unexpected error: " . $e->getMessage());
    return false;
}
```

## 2. WordPress Specific Standards

### 2.1 Database
```php
// Always use $wpdb->prepare()
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_status = %s AND post_type = %s",
        'publish',
        'custom_post_type'
    )
);

// Never concatenate user input into SQL
$bad = "SELECT * FROM posts WHERE ID = " . $_GET['id']; // DANGER!
$good = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$wpdb->posts} WHERE ID = %d", absint($_GET['id'])));
```

### 2.2 Options API
```php
// Update option (autoloaded)
update_option('[plugin_name]_settings', $settings);

// Update option (not autoloaded)
update_option('[plugin_name]_large_data', $data, 'no');

// Delete option
delete_option('[plugin_name]_temp_setting');

// Get with default
$settings = get_option('[plugin_name]_settings', ['default_key' => 'default_value']);
```

### 2.3 Transients API
```php
// Set transient (expires in 1 hour)
set_transient('[plugin_name]_cached_data', $data, HOUR_IN_SECONDS);

// Get transient
$data = get_transient('[plugin_name]_cached_data');
if (false === $data) {
    $data = $this->fetch_data_from_db();
    set_transient('[plugin_name]_cached_data', $data, HOUR_IN_SECONDS);
}

// Delete transient
delete_transient('[plugin_name]_cached_data');
```

### 2.4 Hooks
```php
// Actions
add_action('wp_enqueue_scripts', [$this, 'enqueue_assets']);
add_action('init', '[plugin_name]_register_post_types');
remove_action('wp_head', 'rsd_link');

// Filters
add_filter('template_include', [$this, 'custom_template']);
add_filter('posts_where', [$this, 'filter_posts']);
$filtered = apply_filters('[plugin_name]_item_data', $item_data);

// Priority and accepted args
add_action('wp_enqueue_scripts', [$this, 'enqueue_assets'], 10, 0);
add_filter('the_content', 'process_content', 10, 1);
```

### 2.5 Global Variables
```php
// Always declare global before use
function [namespace]_process_item() {
    global $wpdb, $post;
    
    $table_name = $wpdb->prefix . '[plugin_name]_items';
    $post_id = $post->ID;
}
```

## 3. Security Standards

### 3.1 Nonces
```php
// Generate nonce
$nonce = wp_create_nonce('[plugin_name]_action');

// Verify nonce
if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], '[plugin_name]_action')) {
    wp_die(__('Security check failed', '[text_domain]'));
}

// Nonce in URL
wp_nonce_url(admin_url('admin-ajax.php?action=[plugin_name]_delete_item'), '[plugin_name]_delete_item_' . $item_id);
```

### 3.2 Capability Checks
```php
// Check capabilities before actions
if (!current_user_can('edit_posts')) {
    wp_die(__('Insufficient permissions', '[text_domain]'));
}

// Role-based checks
if (!current_user_can('administrator')) {
    return;
}

// Custom capability
if (!current_user_can('manage_items')) {
    wp_die(__('You do not have permission to manage items', '[text_domain]'));
}
```

### 3.3 Sanitization
```php
// Text fields
$sanitized = sanitize_text_field($_POST['field']);

// Email
$email = sanitize_email($_POST['email']);

// URL
$url = esc_url_raw($_POST['url']);

// Integer
$id = absint($_GET['id']);

// Hex color
$color = sanitize_hex_color($_POST['color']);

// Textarea
$description = sanitize_textarea_field($_POST['description']);

// HTML (allow specific tags)
$allowed_html = [
    'a' => ['href' => true, 'title' => true],
    'strong' => [],
    'em' => [],
];
$html = wp_kses($_POST['html'], $allowed_html);
```

### 3.4 Escaping
```php
// Output to HTML
echo esc_html($title);
echo esc_html__($translatable_text, '[text_domain]');
echo esc_html_x($context_text, 'context', '[text_domain]');

// Output to attribute
echo esc_attr($class);

// Output URL
echo esc_url($permalink);
echo esc_url_raw($api_url);

// Output in JavaScript (use wp_localize_script or wp_add_inline_script)
wp_add_inline_script('[plugin_name]-script', 'var data = ' . wp_json_encode($data) . ';');
```

## 4. Performance Standards

### 4.1 Database Queries
```php
// Use WP_Query instead of $wpdb when possible
$query = new WP_Query([
    'post_type' => 'custom_post_type',
    'posts_per_page' => 10,
    'post_status' => 'publish',
]);

// When using $wpdb directly
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} p
         INNER JOIN {$wpdb->postmeta} m ON p.ID = m.post_id
         WHERE m.meta_key = %s AND m.meta_value = %s",
        '[plugin_name]_meta_key',
        'meta_value'
    )
);

// Use FOUND_ROWS() for pagination
$results = $wpdb->get_results($query);
$total = $wpdb->get_var('SELECT FOUND_ROWS()');
```

### 4.2 Object Caching
```php
// Set cache
wp_cache_set('[plugin_name]_items_' . $category, $items, '[plugin_name]', 3600);

// Get cache
$items = wp_cache_get('[plugin_name]_items_' . $category, '[plugin_name]');
if (false === $items) {
    $items = $this->fetch_items($category);
    wp_cache_set('[plugin_name]_items_' . $category, $items, '[plugin_name]', 3600);
}

// Delete cache (when data changes)
wp_cache_delete('[plugin_name]_items_' . $category, '[plugin_name]');
wp_cache_flush_group('[plugin_name]'); // WordPress 6.0+
```

### 4.3 Autoloaded Options
```php
// Check autoloaded data size
function [namespace]_check_autoloaded_size() {
    global $wpdb;
    $results = $wpdb->get_results("
        SELECT option_name, LENGTH(option_value) as size
        FROM {$wpdb->options}
        WHERE autoload = 'yes'
        ORDER BY size DESC
        LIMIT 10
    ");
    
    $total = 0;
    foreach ($results as $row) {
        $total += $row->size;
        echo sprintf('%s: %s bytes (%.2f MB)', $row->option_name, $row->size, $row->size / 1024 / 1024) . PHP_EOL;
    }
    echo 'Total: ' . number_format($total / 1024 / 1024, 2) . ' MB' . PHP_EOL;
}

// Never autoload large data
update_option('[plugin_name]_large_export', $data, 'no');

// Use transients for temporary data
set_transient('[plugin_name]_api_response', $response, DAY_IN_SECONDS);
```

### 4.4 Query Optimization
```php
// Use fields => IDs for performance
$query = new WP_Query([
    'post_type' => 'custom_post_type',
    'fields' => 'ids',
    'no_found_rows' => true, // When pagination not needed
]);

// Use get_posts() for simple queries
$items = get_posts([
    'post_type' => 'custom_post_type',
    'numberposts' => 5,
    'post_status' => 'publish',
]);

// Avoid SELECT * when using $wpdb
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT post_title, post_name FROM {$wpdb->posts} WHERE post_type = %s",
        'custom_post_type'
    )
);
```

## 5. Frontend Standards

### 5.1 Asset Registration
```php
public function enqueue_assets() {
    // CSS
    wp_register_style(
        '[plugin_name]-style',
        PLUGIN_URL . 'assets/dist/css/style.css',
        [],
        PLUGIN_VERSION
    );
    
    // JS
    wp_register_script(
        '[plugin_name]-script',
        PLUGIN_URL . 'assets/dist/js/script.js',
        ['jquery'],
        PLUGIN_VERSION,
        true // In footer
    );
    
    // Localize script
    wp_localize_script('[plugin_name]-script', '[PluginNamespace]', [
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('[plugin_name]_nonce'),
        'i18n' => [
            'search_placeholder' => __('Search...', '[text_domain]'),
            'no_results' => __('No results found', '[text_domain]'),
        ],
    ]);
    
    // Enqueue
    wp_enqueue_style('[plugin_name]-style');
    wp_enqueue_script('[plugin_name]-script');
}
```

### 5.2 Conditional Loading
```php
// Only load on specific pages
public function enqueue_assets() {
    if (!is_post_type_archive('custom_post_type')) {
        return;
    }
    
    wp_enqueue_script('[plugin_name]-script');
}

// Only load on frontend
public function enqueue_assets() {
    if (is_admin()) {
        return;
    }
    
    wp_enqueue_style('[plugin_name]-style');
}
```

### 5.3 BEM CSS Structure
```scss
.[plugin-name]-card {
    &__image {
        width: 100%;
        height: auto;
    }
    
    &__content {
        padding: var(--spacing-md);
    }
    
    &--featured {
        border: 2px solid var(--color-primary);
    }
    
    &--compact {
        display: flex;
        flex-direction: row;
    }
}
```

## 6. Testing Standards

### 6.1 Unit Tests
```php
class ItemHandlerTest extends WP_UnitTestCase {
    public function setUp(): void {
        parent::setUp();
        $this->handler = new \[Namespace]\Plugin\Handler();
    }
    
    public function test_get_item_returns_model() {
        $post_id = $this->factory->post->create([
            'post_type' => 'custom_post_type',
        ]);
        
        $item = $this->handler->get_item($post_id);
        
        $this->assertInstanceOf(\[Namespace]\Plugin\Item_Model::class, $item);
        $this->assertEquals($post_id, $item->get_id());
    }
    
    public function test_get_item_returns_null_for_invalid_id() {
        $item = $this->handler->get_item(99999);
        $this->assertNull($item);
    }
}
```

### 6.2 Integration Tests
```php
class ShortcodeIntegrationTest extends WP_UnitTestCase {
    public function test_shortcode_render() {
        $shortcode = new \[Namespace]\Plugin\Shortcodes\ItemListShortcode();
        $output = $shortcode->render(['limit' => '5'], '');
        
        $this->assertStringContainsString('[plugin-name]-style', $output);
        $this->assertStringNotContainsString('PHP Notice', $output);
    }
}
```

### 6.3 PHPUnit Configuration
```xml
<!-- phpunit.xml.dist -->
<?xml version="1.0"?>
<phpunit
    bootstrap="tests/bootstrap.php"
    backupGlobals="false"
    colors="true"
    convertErrorsToExceptions="true"
    convertNoticesToExceptions="true"
    convertWarningsToExceptions="true"
>
    <testsuites>
        <testsuite name="[Plugin] Tests">
            <directory suffix="Test.php">./tests</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

## 7. Internationalization

### 7.1 Text Domain
```php
// Always use consistent text domain
define('PLUGIN_TEXT_DOMAIN', '[text_domain]');

// Translate strings
echo __('Hello World', '[text_domain]');
echo esc_html__('Search items', '[text_domain]');

// Contextual translation
echo esc_html_x('Post', 'item post', '[text_domain]');

// Plural strings
$count = 5;
echo sprintf(
    _n('%s item', '%s items', $count, '[text_domain]'),
    number_format($count)
);

// Translatable with variables
printf(
    __('Item #%d: %s', '[text_domain]'),
    $item_id,
    esc_html($item_name)
);
```

### 7.2 Loading Text Domain
```php
public function load_textdomain() {
    load_plugin_textdomain('[text_domain]', false, dirname(plugin_basename(__FILE__)) . '/languages');
}
add_action('plugins_loaded', [$this, 'load_textdomain']);
```

## 8. Documentation Standards

### 8.1 PHPDoc Blocks
```php
/**
 * Get item by ID
 *
 * @param int    $id      Item post ID
 * @param bool   $cache   Whether to use cache (default true)
 * @param string $context Query context (default 'view')
 * @return Item_Model|null Item model or null if not found
 * @throws \InvalidArgumentException If ID is not a positive integer
 */
public function get_item(int $id, bool $cache = true, string $context = 'view'): ?Item_Model {
    if ($id <= 0) {
        throw new \InvalidArgumentException('ID must be a positive integer');
    }
    
    // Implementation
}
```

### 8.2 Function Documentation
```php
/**
 * Register custom post type
 *
 * Creates the custom post type with appropriate
 * labels, capabilities, and rewrite rules.
 *
 * @return void
 */
function [namespace]_register_custom_post_type(): void {
    // Implementation
}
```

## 9. Changelog Format

```
== 1.0.5 ==
* Fix: Item list pagination issue on page 2+
* Add: Support for category filtering
* Add: REST endpoint for item search
* Update: Database schema for new fields
* Improve: Cache invalidation for item updates
* Security: Sanitize AJAX input parameters

== 1.0.4 ==
* Fix: Memory leak in export feature
* Add: Cron job for daily stats aggregation
```
