#!/bin/haserl
<%in _common.cgi %>
<%
page_title="Send to MQTT"

[ -f /usr/bin/mosquitto_pub ] || redirect_to "/" "danger" "MQTT client is not a part of your firmware."

defaults() {
	default_for mqtt_client_id "${network_macaddr//:/}"
	default_for mqtt_port "1883"
	default_for mqtt_topic "thingino/$mqtt_client_id"
	default_for mqtt_message ""
}

if [ "POST" = "$REQUEST_METHOD" ]; then
	error=""

	read_from_post "mqtt" "host port client_id username password topic message send_snap snap_topic use_ssl"

	error_if_empty "$mqtt_host" "MQTT broker host cannot be empty."
	error_if_empty "$mqtt_port" "MQTT port cannot be empty."
	# error_if_empty "$mqtt_username" "MQTT username cannot be empty."
	# error_if_empty "$mqtt_password" "MQTT password cannot be empty."
	error_if_empty "$mqtt_topic" "MQTT topic cannot be empty."
	error_if_empty "$mqtt_message" "MQTT message cannot be empty."

	if [ "${mqtt_topic:0:1}" = "/" ] || [ "${mqtt_snap_topic:0:1}" = "/" ]; then
		set_error_flag "MQTT topic should not start with a slash."
	fi

	if [ "$mqtt_topic" != "${mqtt_topic// /}" ] || [ "$mqtt_snap_topic" != "${mqtt_snap_topic// /}" ]; then
		set_error_flag "MQTT topic should not contain spaces."
	fi

	if [ -n "$(echo $mqtt_topic | sed -r -n /[^a-zA-Z0-9/]/p)" ] || [ -n "$(echo $mqtt_snap_topic | sed -r -n /[^a-zA-Z0-9/]/p)" ]; then
		set_error_flag "MQTT topic should not include non-ASCII characters."
	fi

	if [ "true" = "$mqtt_send_snap" ] && [ -z "$mqtt_snap_topic" ]; then
		set_error_flag "MQTT topic for snapshot should not be empty."
	fi

	defaults

	if [ -z "$error" ]; then
		save2config "
mqtt_client_id=\"$mqtt_client_id\"
mqtt_host=\"$mqtt_host\"
mqtt_message=\"$mqtt_message\"
mqtt_password=\"$mqtt_password\"
mqtt_port=\"$mqtt_port\"
mqtt_send_snap=\"$mqtt_send_snap\"
mqtt_snap_topic=\"$mqtt_snap_topic\"
mqtt_topic=\"$mqtt_topic\"
mqtt_use_ssl=\"$mqtt_use_ssl\"
mqtt_username=\"$mqtt_username\"
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
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3">
<div class="col">
<% field_text "mqtt_client_id" "MQTT client ID" %>
<div class="row g-1">
<div class="col-10"><% field_text "mqtt_host" "MQTT broker FQDN or IP address" %></div>
<div class="col-2"><% field_text "mqtt_port" "Port" %></div>
</div>
<% field_text "mqtt_username" "MQTT broker username" %>
<% field_password "mqtt_password" "MQTT broker password" %>
<% field_switch "mqtt_use_ssl" "Use SSL" %>
</div>
<div class="col">
<% field_text "mqtt_topic" "MQTT topic" %>
<% field_textarea "mqtt_message" "MQTT message" "$STR_SUPPORTS_STRFTIME" %>
<% field_switch "mqtt_send_snap" "Send a snapshot" %>
<% field_text "mqtt_snap_topic" "MQTT topic to send the snapshot to" %>
</div>
</div>
<% button_submit %>
</form>

<div class="alert alert-dark ui-debug d-none">
<h4 class="mb-3">Debug info</h4>
<% ex "grep ^mqtt_ $CONFIG_FILE" %>
</div>

<script>
$('#mqtt_message').style.height = '7rem';
$('#mqtt_use_ssl').addEventListener('change', ev => {
	const el=$('#mqtt_port');
	if (ev.target.checked) {
		if (el.value === '1883') el.value='8883';
	} else {
		if (el.value === '8883') el.value='1883';
	}
});
</script>

<%in _footer.cgi %>
