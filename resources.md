---
title: Resources
description: These are sites that I've found over the years to help with various things.
permalink: /resources/
---
{% for resource in site.resources %}
<div class="in-resources {{ resource.title | strip | replace: ' ','-' | downcase | append: '-page' }}">
	<h3>
		{% if resource.nocaps %}
		{{ resource.title }}
		{% endif %}
		{% unless resource.nocaps %}
		{{ resource.title | capitalize }}
		{% endunless %}
	</h3>
	{{ resource.content | markdownify }}
</div>
{% endfor %}
