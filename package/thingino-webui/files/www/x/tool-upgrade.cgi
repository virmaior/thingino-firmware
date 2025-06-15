#!/bin/haserl --upload-limit=43008 --upload-dir=/tmp
<%in _common.cgi %>
<%
page_title="Flash Operations"

tools_action="sysupgrade"
tools_upgrade_option="-p"
ota_upgrade_option="Partial"
tools_upgrade_option="Partial"
mtdblock_partition="mtd0"

if [ "$REQUEST_METHOD" = "POST" ]; then
	if [ -n "$HASERL_firmware_path" ]; then
		mv "$HASERL_firmware_path" /tmp/fw-web.bin
		echo "Content-Type: application/json"
		echo
		echo '{"success": true}'
		exit 0
	fi
fi

if [ "$QUERY_STRING" = "action=generate_backup" ]; then
	host=$(hostname)
	current_date=$(date +%Y-%m-%d)
	echo "Content-Type: application/octet-stream"
	echo "Content-Disposition: attachment; filename=backup-${host}-${current_date}.tar.gz"
	echo
	tar -cf - /etc | gzip
	exit 0
fi

if [ ! -z "$QUERY_STRING" ]; then
	if echo "$QUERY_STRING" | grep -q "^partition="; then
		partition=$(echo "$QUERY_STRING" | sed -n 's/^partition=//p')
		if [ -n "$partition" ] && [ -e "/dev/$partition" ]; then
			echo "Content-Type: application/octet-stream"
			echo "Content-Disposition: attachment; filename=$partition.bin"
			echo
			cat "/dev/$partition"
			exit 0
		else
			echo "Content-Type: text/plain"
			echo
			echo "Error: Invalid or missing partition."
			exit 1
		fi
	fi
fi

get_mtd_partitions() {
	awk -F: '/^mtd[0-9]+/ {print $1}' /proc/mtd | tr '\n' ',' | sed 's/,$//'
}
%>
<%in _header.cgi %>

<div class="row g-4">
<div class="col col-lg-4">
<div class="alert alert-success">
<h4>Backup</h4>
<p>Click "Generate archive" button to download a tar archive of the current configuration files.</p>
<button class="btn btn-primary" id="button-backup">Generate archive</button>
</div>

<div class="alert alert-info">
<h4>Save mtdblock contents</h4>
<p>Click "Save mtdblock" to download the specified mtdblock file. (NOTE: THIS FEATURE IS FOR PROFESSIONALS!)</p>
<% field_select "mtdblock_partition" "Choose mtdblock" "$(get_mtd_partitions)" %>
<button type="button" class="btn btn-primary" id="button-mtdblock">Save mtdblock</button>
</div>

<div class="alert alert-warning">
<h4>OTA (Over The Air) Update</h4>
<p>Click to perform an upgrade to the latest firmware release from the Thingino GitHub repository.</p>
<% field_select "ota_upgrade_option" "Upgrade Option" "Partial,Full,Bootloader" %>
<button type="button" class="btn btn-primary" id="button-upgrade">Download & Upgrade</button>
</div>

<div class="alert alert-danger">
<h4>Flash new firmware image</h4>
<p>Upload a sysupgrade-compatible image here to replace the current firmware</p>
<input type="file" class="form-control" id="firmware-image" name="firmware">
<button type="button" class="btn btn-primary mt-2" id="button-upload">Flash image</button>
</div>
</div>
<div class="col col-lg-8">
<div id="output-wrapper" class="p-1">
<pre class="m-0 h-100"></pre>
</div>
</div>
</div>

<style>
#output-wrapper {
	display: none;
	background-color: #000;
	border-radius: 0.5rem;
	color: #fff;
	height: calc(100vh - 200px);
	padding: 1rem;
	overflow-y: auto;
}
pre {
	white-space:pre-wrap;
	word-wrap:break-word;
}
</style>

<script>
async function handleOTAUpgrade() {
	const wr = $('#output-wrapper');
	if (!wr) return;

	wr.style.display = 'block';
	wr.innerHTML = '';

	let cmd='touch /tmp/webupgrade;/sbin/sysupgrade ';
	const option = $('#ota_upgrade_option').value;
	if (option === 'Full') {
		cmd += '-f';
	} else if (option === 'Bootloader') {
		cmd += '-b';
	} else {
		cmd += '-p';
	}

	const el = document.createElement('pre');
	el.id = 'output';
	el.dataset.cmd = cmd;
	el.style.margin = '0';
	el.style.whiteSpace = 'pre-wrap';
	el.style.wordWrap = 'break-word';

	const h6 = document.createElement('h6');
	h6.textContent = '# ' + cmd;
	h6.style.margin = '0 0 1rem 0';

	wr.appendChild(h6);
	wr.appendChild(el);

	await streamOutput(el, cmd);
}

async function handleUpgrade(ev) {
	if (ev) ev.preventDefault();

	const fileInput = $('#firmware-image');
	if (!fileInput || !fileInput.files || !fileInput.files.length) {
		return; // Early return if no file selected
	}

	const submitButton = $('#button-upload');
	if (submitButton) submitButton.disabled = true;

	const wr = $('#output-wrapper');
	if (!wr) {
		if (submitButton) submitButton.disabled = false;
		return;
	}

	wr.style.display = 'block';
	wr.innerHTML = '';
	let cmd = '/sbin/sysupgrade';

	const uploadStatus = document.createElement('pre');
	uploadStatus.style.margin = '0';
	uploadStatus.style.whiteSpace = 'pre-wrap';
	uploadStatus.style.wordWrap = 'break-word';
	uploadStatus.textContent = 'Uploading firmware file...';
	wr.appendChild(uploadStatus);

	const formData = new FormData();
	formData.append('firmware', fileInput.files[0]);

	try {
		const response = await fetch(window.location.pathname, {
		    method: 'POST',
		    body: formData
		});

		if (!response.ok) throw new Error('Upload failed: ' + response.statusText);
		cmd += ' /tmp/fw-web.bin';
		wr.innerHTML = '';
	} catch (error) {
		uploadStatus.textContent = 'Upload failed: ' + error.message;
		if (submitButton) submitButton.disabled = false;
		return;
	}

	const el = document.createElement('pre');
	el.id = 'output';
	el.dataset.cmd = cmd;
	el.style.margin = '0';
	el.style.whiteSpace = 'pre-wrap';
	el.style.wordWrap = 'break-word';

	const h6 = document.createElement('h6');
	h6.textContent = '# ' + cmd;
	h6.style.margin = '0 0 1rem 0';

	wr.appendChild(h6);
	wr.appendChild(el);

	await streamOutput(el, cmd);
}

async function streamOutput(el, cmd) {
	async function* makeTextFileLineIterator(url) {
		const td = new TextDecoder('utf-8');
		const response = await fetch(url);
		const rd = response.body.getReader();
		let { value: chunk, done: readerDone } = await rd.read();
		chunk = chunk ? td.decode(chunk) : '';
		const re = /\n|\r|\r\n/gm;
		let startIndex = 0;
		let result;
		try {
			for (;;) {
				result = re.exec(chunk);
				if (!result) {
					if (readerDone) break;
					let remainder = chunk.substr(startIndex);
					({ value: chunk, done: readerDone } = await rd.read());
					chunk = remainder + (chunk ? td.decode(chunk) : '');
					startIndex = re.lastIndex = 0;
					continue;
				}
				yield chunk.substring(startIndex, result.index);
				startIndex = re.lastIndex;
			}
			if (startIndex < chunk.length) yield chunk.substr(startIndex);
		} finally {
			el.innerHTML += '\n--- sysupgrade exit! ---\n';
			// Only re-enable the flash button if we are in the manual upload flow
			if (cmd.includes('/tmp/fw-web.bin'))
				$('#button-upload').disabled = false;
		}
	}

	let lastProgressLine = '';
	let lines = [];

	for await (let line of makeTextFileLineIterator('/x/run.cgi?cmd=' + btoa(cmd))) {
		line = line.trimEnd() + '</span>';

		line = line
			.replace(/\[38;5;(\d+)m/g, '</span><span style="color: var(--ansi-$1);">')
			.replace(/\[(\d+)m/g, '</span><span class="ansi-$1">')
			.replace(/\[0m/g, '</span>')
			.replace(/\x1B/g, '')
			.replace(/[\x00-\x1F\x7F-\x9F]/g, '');

		if (line.includes('Writing kb:') ||
			line.includes('Verifying kb:') ||
			line.match(/^[#O-]+\s+\d+\.?\d*%/) ||
			line.match(/^#+\s+\d+\.?\d*%/) ||
			line.match(/^#[#O=\-]+.*/) ||
			line.match(/^Erasing block: \d+\/\d+ \(\d+%\)/)) {
			if (lastProgressLine) {
				lines[lines.length - 1] = line;
			} else {
				lines.push(line);
			}
			lastProgressLine = line;
		} else if (line.trim()) {
			lastProgressLine = '';
			lines.push(line);
		}

		el.innerHTML = lines.join('\n');
		const wr = $('#output-wrapper');
		if (wr) wr.scrollTop = wr.scrollHeight;
	}
}

$('#button-backup').addEventListener('click', ev => {
	window.location.href = window.location.pathname + '?action=generate_backup'
})

$('#button-mtdblock').addEventListener('click', ev => {
	const partition = $('#mtdblock_partition').value;
	if (partition) {
		window.location.href = window.location.pathname + '?partition=' + partition
	} else {
		alert('Please select an mtdblock partition.')
	}
})

$('#button-upgrade').addEventListener('click', handleOTAUpgrade)

$('#button-upload').addEventListener('click', handleUpgrade)

$('#firmware-image').addEventListener('change', ev => $('#button-upload').disabled = (ev.target.files.length == 0))

$('#button-upload').disabled = true
</script>

<%in _footer.cgi %>
