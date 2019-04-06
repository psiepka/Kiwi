<h1>Currency converter</h1>
<hr>
<br><br>
<h3>Contain:</h3>
<ul>
    <li>
        CLI application
    </li>
    <li>
        web API application
    </li>
</ul>
<small>All tested.</small>
<hr>
<h3>Functionality:</h3>
<ul>
    <li>
        converting currency for 170 world currencies
    </li>
    <li>
        use <a href="https://fixer.io/">https://fixer.io/</a> for real-time currencies
    </li>
    <li>
        recognize curriency sign with curriency code
    </li>
</ul>
<hr>
<h3>Quickstart</h3>
<br>
<p>If you want to try it, you must have <b>free</b> acces key to fixier API</p>
<br><br>
<h4>Install:</h4><br>
<code>git clone https://github.com/psiepka/Kiwi.git</code><br>
<small>create <b>.env</b> file with ACCES_KEY</small><br>
<code>echo ACCES_KEY=&lt;your-acces-key&gt; > .env</code><br>
<code>python3 -m venv venv</code><br>
<code>venv\Scripts\activate</code><br>
<code>pip install -r requirements.txt</code><br><br>
<b>Done !</b>
<br><br>
<h5>Web Aplication</h5>
<p>to start it you must only start <b>web_app.py</b></p>
<br>
<b>Example</b><br>
<pre>
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
{
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20,
    }
}
</pre>
<pre>
GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
    {
        "input": {
            "amount": 10.92,
            "currency": "GBP"
        },
        "output": {
            "EUR": 14.95,
            "USD": 17.05,
            "CZK": 404.82,
            .
            .
            .
        }
    }
</pre>
<br><br>
<h5>CLI Aplication</h5>
<p>to start it you must only start <b>currency_converter.py</b></p>
<br>
<b>Example</b><br>
<pre>
python3 currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
    {
        "input": {
            "amount": 100.0,
            "currency": "EUR"
        },
        "output": {
            "CZK": 2707.36,
        }
    }
</pre>
<pre>
python3 currency_converter.py --amount 10.92 --input_currency £
    {
        "input": {
            "amount": 10.92,
            "currency": "GBP"
        },
        "output": {
            "EUR": 14.95,
            "USD": 17.05,
            "CZK": 404.82,
            .
            .
            .
        }
    }
</pre>
