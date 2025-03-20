#!/bin/haserl
<%in _common.cgi %>
<%
page_title="Day/Night Mode Control"

DAYNIGHT_APP="daynight"

# read settings from crontab
grep -q "^[^#].*$DAYNIGHT_APP\$" $CRONTABS && day_night_enabled=true
day_night_interval=$(awk -F'[/ ]' "/$DAYNIGHT_APP\$/{print \$2}" $CRONTABS)

defaults() {
	default_for day_night_interval "1"
	default_for day_night_max "15000"
	default_for day_night_min "5000"
	default_for day_night_color "false"
	default_for day_night_ircut "false"
	default_for day_night_ir850 "false"
	default_for day_night_ir940 "false"
	default_for day_night_white "false"
	default_for dusk2dawn_offset_sr "0"
	default_for dusk2dawn_offset_ss "0"
}

if [ "POST" = "$REQUEST_METHOD" ]; then
	error=""

	read_from_post "day_night" "color enabled interval ir850 ir940 ircut max min white"
	read_from_post "dusk2dawn" "enabled lat lng offset_sr offset_ss"

	defaults

	# validate
	if [ "true" = "$day_night_enabled" ]; then
		error_if_empty "$day_night_min" "Day mode threshold cannot be empty"
		error_if_empty "$day_night_max" "Night mode threshold cannot be empty"
	fi

	if [ "true" = "$dusk2dawn_enabled" ]; then
		error_if_empty "$dusk2dawn_lat" "Latitude cannot be empty"
		error_if_empty "$dusk2dawn_lng" "Longitude cannot be empty"
	fi

	if [ -z "$error" ]; then
		save2config "
day_night_color=\"$day_night_color\"
day_night_enabled=\"$day_night_enabled\"
day_night_interval=\"$day_night_interval\"
day_night_ir850=\"$day_night_ir850\"
day_night_ir940=\"$day_night_ir940\"
day_night_ircut=\"$day_night_ircut\"
day_night_max=\"$day_night_max\"
day_night_min=\"$day_night_min\"
day_night_white=\"$day_night_white\"
dusk2dawn_enabled=\"$dusk2dawn_enabled\"
dusk2dawn_lat=\"$dusk2dawn_lat\"
dusk2dawn_lng=\"$dusk2dawn_lng\"
dusk2dawn_offset_sr=\"$dusk2dawn_offset_sr\"
dusk2dawn_offset_ss=\"$dusk2dawn_offset_ss\"
"
		# update crontab
		tmpfile=$(mktemp -u)
		cat $CRONTABS > $tmpfile
		sed -i "/$DAYNIGHT_APP/d" $tmpfile
		echo "# run $DAYNIGHT_APP every $day_night_interval minutes" >> $tmpfile
		[ "true" = "$day_night_enabled" ] || echo -n "#" >> $tmpfile
		echo "*/$day_night_interval * * * * $DAYNIGHT_APP" >> $tmpfile
		mv $tmpfile $CRONTABS

		if [ "true" = "$dusk2dawn_enabled" ]; then
			dusk2dawn > /dev/null
		fi
		redirect_to $SCRIPT_NAME "success" "Data updated."
	else
		redirect_to $SCRIPT_NAME "danger" "Error: $error"
	fi
fi

defaults
%>
<%in _header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post" class="mb-3">
<div class="row row-cols-1 row-cols-md-2 row-cols-xxl-4 mb-4">

<div class="col">
<h3 class="alert alert-warning text-center">Gain <span class="gain"></span></h3>
<% field_number "day_night_min" "Switch to Day mode when gain drops below" %>
<% field_number "day_night_max" "Switch to Night mode when gain raises above" %>
</div>

<div class="col mb-3">
<h3>By Illumination</h3>
<% field_switch "day_night_enabled" "Enable Day/Night script" %>
<p>Run with <a href="info.cgi?crontab">cron</a> every <input type="text" id="day_night_interval"
name="day_night_interval" value="<%= $day_night_interval %>" pattern="[0-9]{1,}" title="numeric value"
class="form-control text-end" data-min="1" data-max="60" data-step="1"> min.</p>

<h5>Actions to perform</h5>
<% field_checkbox "day_night_color" "Change color mode" %>
<% [ -z "$gpio_ircut" ] || field_checkbox "day_night_ircut" "Flip IR cut filter" %>
<% [ -z "$gpio_ir850" ] || field_checkbox "day_night_ir850" "Toggle IR 850 nm" %>
<% [ -z "$gpio_ir940" ] || field_checkbox "day_night_ir940" "Toggle IR 940 nm" %>
<% [ -z "$gpio_white" ] || field_checkbox "day_night_white" "Toggle white light" %>
</div>

<div class="col">
<h3>By Sun</h3>
<% field_switch "dusk2dawn_enabled" "Enable Sun tracking" %>
<div class="row g-1">
<div class="col"><% field_text "dusk2dawn_lat" "Latitude"  %></div>
<div class="col"><% field_text "dusk2dawn_lng" "Longitude" %></div>
</div>
<p><a href="https://my-coordinates.com/">Find your coordinates</a></p>
<div class="row g-1">
<div class="col"><% field_text "dusk2dawn_offset_sr" "Sunrise offset" "minutes" %></div>
<div class="col"><% field_text "dusk2dawn_offset_ss" "Sunset offset" "minutes" %></div>
</div>
</div>

<div class="col">
<div class="alert alert-info">
<p>The day/night mode is controlled by the brightness of the scene.
Changes in illumination affect the gain required to normalise a darkened image - the darker the scene, the higher the gain value.
The current gain value is displayed at the top of each page next to the sun emoji.
Switching between modes is triggered by changes in the gain beyond the threshold values.</p>
<% wiki_page "Configuration:-Night-Mode" %>
</div>
</div>
</div>

<% button_submit %>
</form>

<div class="alert alert-dark ui-debug d-none">
<h4 class="mb-3">Debug info</h4>
<% ex "grep ^day_night_ $CONFIG_FILE" %>
<% ex "grep ^dusk2dawn_ $CONFIG_FILE" %>
<% ex "crontab -l" %>
</div>

<%in _footer.cgi %>
