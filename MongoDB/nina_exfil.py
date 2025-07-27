import requests
from flask import Flask, Response

app = Flask(__name__)

NINA_GRAPH_URL = "http://192.168.1.138:1888/v2/api/equipment/guider/graph"
NINA_MOUNT_URL = "http://192.168.1.138:1888/v2/api/equipment/mount/info"

@app.route("/metrics")
def metrics():
    output = ""

    # ------- Guider Metrics -------
    try:
        r = requests.get(NINA_GRAPH_URL, timeout=5)
        graph_data = r.json().get("Response", {})
        rms = graph_data.get("RMS", {})
        guide_steps = graph_data.get("GuideSteps", [])

        last_ra = guide_steps[-1].get("RADistanceRaw", 0.0) if guide_steps else 0.0
        last_dec = guide_steps[-1].get("DECDistanceRaw", 0.0) if guide_steps else 0.0

        output += f"""
# HELP nina_guide_error_ra Last RA guiding error
# TYPE nina_guide_error_ra gauge
nina_guide_error_ra {last_ra}

# HELP nina_guide_error_dec Last DEC guiding error
# TYPE nina_guide_error_dec gauge
nina_guide_error_dec {last_dec}

# HELP nina_guide_rms_ra RMS error RA
# TYPE nina_guide_rms_ra gauge
nina_guide_rms_ra {rms.get("RA", 0.0)}

# HELP nina_guide_rms_dec RMS error DEC
# TYPE nina_guide_rms_dec gauge
nina_guide_rms_dec {rms.get("Dec", 0.0)}

# HELP nina_guide_rms_total RMS total
# TYPE nina_guide_rms_total gauge
nina_guide_rms_total {rms.get("Total", 0.0)}

# HELP nina_guide_peak_ra Peak RA error
# TYPE nina_guide_peak_ra gauge
nina_guide_peak_ra {rms.get("PeakRA", 0.0)}

# HELP nina_guide_peak_dec Peak DEC error
# TYPE nina_guide_peak_dec gauge
nina_guide_peak_dec {rms.get("PeakDec", 0.0)}
"""
    except Exception as e:
        output += f"# Error fetching guider data: {e}\n"

    # ------- Mount Metrics -------
    try:
        r = requests.get(NINA_MOUNT_URL, timeout=5)
        mount = r.json().get("Response", {})
        coords = mount.get("Coordinates", {})
        datetime = coords.get("DateTime", {})

        output += f"""
# HELP nina_mount_ra Right Ascension (hours)
# TYPE nina_mount_ra gauge
nina_mount_ra {mount.get("RightAscension", 0.0)}

# HELP nina_mount_dec Declination (degrees)
# TYPE nina_mount_dec gauge
nina_mount_dec {mount.get("Declination", 0.0)}

# HELP nina_mount_altitude Telescope altitude (degrees)
# TYPE nina_mount_altitude gauge
nina_mount_altitude {mount.get("Altitude", 0.0)}

# HELP nina_mount_azimuth Telescope azimuth (degrees)
# TYPE nina_mount_azimuth gauge
nina_mount_azimuth {mount.get("Azimuth", 0.0)}

# HELP nina_mount_sidereal_time Sidereal time (hours)
# TYPE nina_mount_sidereal_time gauge
nina_mount_sidereal_time {mount.get("SiderealTime", 0.0)}

# HELP nina_mount_time_to_meridian_flip Time to meridian flip (hours)
# TYPE nina_mount_time_to_meridian_flip gauge
nina_mount_time_to_meridian_flip {mount.get("TimeToMeridianFlip", 0.0)}

# HELP nina_mount_tracking_enabled 1 if tracking is enabled
# TYPE nina_mount_tracking_enabled gauge
nina_mount_tracking_enabled {1 if mount.get("TrackingEnabled") else 0}

# HELP nina_mount_tracking_ra_rate Guide rate in RA (arcsec/sec)
# TYPE nina_mount_tracking_ra_rate gauge
nina_mount_tracking_ra_rate {mount.get("GuideRateRightAscensionArcsecPerSec", 0.0)}

# HELP nina_mount_tracking_dec_rate Guide rate in DEC (arcsec/sec)
# TYPE nina_mount_tracking_dec_rate gauge
nina_mount_tracking_dec_rate {mount.get("GuideRateDeclinationArcsecPerSec", 0.0)}

# HELP nina_mount_slewing 1 if slewing
# TYPE nina_mount_slewing gauge
nina_mount_slewing {1 if mount.get("Slewing") else 0}

# HELP nina_mount_at_park 1 if parked
# TYPE nina_mount_at_park gauge
nina_mount_at_park {1 if mount.get("AtPark") else 0}

# HELP nina_mount_at_home 1 if at home position
# TYPE nina_mount_at_home gauge
nina_mount_at_home {1 if mount.get("AtHome") else 0}

# HELP nina_mount_connected 1 if connected
# TYPE nina_mount_connected gauge
nina_mount_connected {1 if mount.get("Connected") else 0}

# HELP nina_mount_pier_east 1 if side of pier is east
# TYPE nina_mount_pier_east gauge
nina_mount_pier_east {1 if mount.get("SideOfPier") == "pierEast" else 0}

# HELP nina_mount_ra_degrees RA in degrees
# TYPE nina_mount_ra_degrees gauge
nina_mount_ra_degrees {coords.get("RADegrees", 0.0)}

# HELP nina_mount_dec_degrees Dec in degrees
# TYPE nina_mount_dec_degrees gauge
nina_mount_dec_degrees {coords.get("Dec", 0.0)}

# HELP nina_mount_site_latitude Latitude of site
# TYPE nina_mount_site_latitude gauge
nina_mount_site_latitude {mount.get("SiteLatitude", 0.0)}

# HELP nina_mount_site_longitude Longitude of site
# TYPE nina_mount_site_longitude gauge
nina_mount_site_longitude {mount.get("SiteLongitude", 0.0)}

# HELP nina_mount_site_elevation Elevation of site (meters)
# TYPE nina_mount_site_elevation gauge
nina_mount_site_elevation {mount.get("SiteElevation", 0.0)}
"""
    except Exception as e:
        output += f"# Error fetching mount data: {e}\n"

    return Response(output.strip(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9101)
