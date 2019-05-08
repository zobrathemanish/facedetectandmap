(function() {
	"use strict";

	if(typeof QuickSettings === "undefined") return;

	var urlMap 	= {
		"Webcam Setup":		"webcam",
		"Picture Setup":	"picture"
	};
	var labels = [];
	for (var key in urlMap) { labels.push(key); } // Fill in the labels.

	function onSetupChosen(data) {
		brfv4Example.init(urlMap[data.value]);
	}

	if(!brfv4Example.gui.setupChooser) {

		QuickSettings.useExtStyleSheet();
	}
})();