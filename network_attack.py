from selenium import webdriver

# Launch Chrome browser
driver = webdriver.Chrome()

# Execute JavaScript code to disable login button and trigger alert on attack
js_code = '''
// Listen for a message indicating a network attack
window.addEventListener('message', function(event) {
    if (event.data === 'network_attack_detected') {
        console.log('Alert: Network attack detected in login page');
        // Disable login button
        document.querySelector('button[type="submit"]').disabled = true;
        // Trigger alert
        alert('Attack initiated. Please contact support.');
        // Close the login page
        window.close();
    }
});
'''

# Open the login page
driver.get("http://127.0.0.1:8000/login/")  

# Inject JavaScript code into the login page
driver.execute_script(js_code)

# Close the browser
driver.quit()
