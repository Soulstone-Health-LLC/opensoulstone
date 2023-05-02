$(function() {
	'use strict'
	var icons = Quill.import('ui/icons');
	icons['bold'] = '<i class="fa fa-bold" aria-hidden="true"><\/i>';
	icons['italic'] = '<i class="fa fa-italic" aria-hidden="true"><\/i>';
	icons['underline'] = '<i class="fa fa-underline" aria-hidden="true"><\/i>';
	icons['strike'] = '<i class="fa fa-strikethrough" aria-hidden="true"><\/i>';
	icons['list']['ordered'] = '<i class="fa fa-list-ol" aria-hidden="true"><\/i>';
	icons['list']['bullet'] = '<i class="fa fa-list-ul" aria-hidden="true"><\/i>';
	icons['link'] = '<i class="fa fa-link" aria-hidden="true"><\/i>';
	icons['image'] = '<i class="fa fa-image" aria-hidden="true"><\/i>';
	icons['video'] = '<i class="fa fa-film" aria-hidden="true"><\/i>';
	icons['code-block'] = '<i class="fa fa-code" aria-hidden="true"><\/i>';
	var toolbarOptions = [
		['bold', 'italic', 'underline', 'strike'],
		[{
			'list': 'ordered'
		}, {
			'list': 'bullet'
		}]
	];
	var quill = new Quill('#quillEditor', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor2', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor3', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor4', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor5', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor6', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor7', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor8', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor9', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	var quill = new Quill('#quillEditor10', {
		modules: {
			toolbar: toolbarOptions
		},
		theme: 'snow'
	});
	new PerfectScrollbar('#scrolling-container', {
		suppressScrollX: true
	});
});