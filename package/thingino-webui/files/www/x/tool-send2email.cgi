#!/bin/haserl
<%in _common.cgi %>
<%
page_title="Send to email"

defaults() {
	default_for email_attach_snapshot "false"
	default_for email_attach_video "true"
	default_for email_from_name "Camera $network_hostname"
	default_for email_insecure_ssl "false"
	default_for email_smtp_port "25"
	default_for email_to_name "Camera admin"
	default_for email_subject "Snapshot from $network_hostname"
}

if [ "POST" = "$REQUEST_METHOD" ]; then
	error=""

	read_from_post "email" "attach_snapshot attach_video from_name from_address insecure_ssl to_name to_address subject body smtp_host smtp_port smtp_username smtp_password smtp_use_ssl"

	# normalize
	email_body="$(echo "$email_body" | tr "\r?\n" " ")"

	error_if_empty "$email_smtp_host" "SMTP host cannot be empty."
	error_if_empty "$email_from_address" "Sender email address cannot be empty."
	error_if_empty "$email_from_name" "Sender name cannot be empty."
	error_if_empty "$email_to_address" "Recipient email address cannot be empty."
	error_if_empty "$email_to_name" "Recipient name cannot be empty."

	defaults

	if [ -z "$error" ]; then
		save2config "
email_attach_snapshot=\"$email_attach_snapshot\"
email_attach_video=\"$email_attach_video\"
email_from_name=\"$email_from_name\"
email_from_address=\"$email_from_address\"
email_insecure_ssl=\"$email_insecure_ssl\"
email_to_name=\"$email_to_name\"
email_to_address=\"$email_to_address\"
email_subject=\"$email_subject\"
email_body=\"$email_body\"
email_smtp_host=\"$email_smtp_host\"
email_smtp_port=\"$email_smtp_port\"
email_smtp_username=\"$email_smtp_username\"
email_smtp_password=\"$email_smtp_password\"
email_smtp_use_ssl=\"$email_smtp_use_ssl\"
"
		redirect_to $SCRIPT_NAME "success" "Data updated."
	else
		redirect_to $SCRIPT_NAME "danger" "Error: $error"
	fi
fi

defaults
%>
<%in _header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post" class="mb-4">
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4 mb-4">
<div class="col">
<div class="row g-1">
<div class="col-10"><% field_text "email_smtp_host" "SMTP server FQDN or IP address" %></div>
<div class="col-2"><% field_text "email_smtp_port" "Port" %></div>
</div>
<% field_text "email_smtp_username" "SMTP username" %>
<% field_password "email_smtp_password" "SMTP password" %>
<% field_switch "email_smtp_use_ssl" "Use TLS/SSL" %>
<% field_switch "email_insecure_ssl" "Ignore SSL certificate validity" %>
</div>
<div class="col">
<% field_text "email_from_name" "Sender's name" "Use a real email address where bounce reports can be sent to." %>
<% field_text "email_from_address" "Sender's address" %>
<% field_text "email_to_name" "Recipient's name" %>
<% field_text "email_to_address" "Recipient's address" %>
</div>
<div class="col">
<% field_text "email_subject" "Email subject" %>
<% field_textarea "email_body" "Email text" "Line breaks will be replaced with whitespaces." %>
<p class="label">Attachment</p>
<% field_switch "email_attach_snapshot" "Attach snapshot" %>
<% field_switch "email_attach_video" "Attach video" %>
</div>
</div>
<% button_submit %>
</form>

<div class="alert alert-dark ui-debug d-none">
<h4 class="mb-3">Debug info</h4>
<% ex "grep ^email_ $CONFIG_FILE" %>
</div>

<script>
$('#email_body').style.height = "6rem";
$('#email_smtp_use_ssl').addEventListener('change', ev => {
	const el=$('#email_smtp_port');
	if (ev.target.checked) {
		if (el.value === "25") el.value="465";
	} else {
		if (el.value === "465") el.value="25";
	}
});
</script>

<%in _footer.cgi %>
