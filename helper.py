#!/usr/bin/env python2

import click
import pyshark
from subprocess import call
from dict import channelFrequencies, phyTypes

def changeToMonitorMode(interface):
	click.secho('-> Setting interface %s to monitor mode' % (interface), fg="cyan")
	call(['systemctl', 'stop', 'NetworkManager'])
	call(['ip', 'link', 'set', interface, 'down'])
	call(['iw', interface, 'set', 'monitor', 'control'])
	call(['ip', 'link', 'set', interface, 'up'])


def changeFrequency(interface, channel):
	freq = str(channelFrequencies[str(channel)])
	click.secho('-> Setting interface %s to monitor on channel %s (%s MHz)' % (interface, channel, freq), fg="cyan")
	call(['iw', 'dev', interface, 'set', 'freq', freq])


def captureBeacons(interface):
	try:
		cap = pyshark.LiveCapture(interface=interface, display_filter="wlan.fc.type_subtype==0x0008")
		for packet in cap:
			click.secho("------------------BEACON-------------------",fg="yellow")
			click.secho(str(packet.frame_info.time),fg="yellow")
			click.secho("SSID: %s" % str(packet.layers[3].ssid),fg="yellow")

			channel = packet.wlan_radio.channel
			frequency = packet.wlan_radio.frequency
			version = phyTypes[packet.wlan_radio.phy]

			click.secho("Channel %s (%s MHz) using %s" % (channel, frequency, version),fg="yellow")

			#pprint(vars(packet.wlan_radio), indent=2)
	except (RuntimeError) as error:
		click.secho('Exited program', fg="cyan")	


def changeToManagedMode(interface):
	click.secho('Setting interface %s to managed mode ' % (interface), fg="cyan")
	call(['ip', 'link', 'set', interface, 'down'])
	call(['iw', interface, 'set', 'type', 'managed'])
	call(['ip', 'link', 'set', interface, 'up'])
	call(['systemctl', 'start', 'NetworkManager'])