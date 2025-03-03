#!/usr/bin/env python3
"""
Flask web application for Perplexity API
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import json
import re
from perplexity_client import query_perplexity

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Store search history in session
def get_search_history():
    if 'search_history' not in session:
        session['search_history'] = []
    return session['search_history']

# Store selected items for next stage
def get_selected_items():
    if 'selected_items' not in session:
        session['selected_items'] = []
    return session['selected_items']

# Store selected URLs for next stage
def get_selected_urls():
    if 'selected_urls' not in session:
        session['selected_urls'] = []
    return session['selected_urls']

# Extract URLs from text
def extract_urls(text):
    # URL regex pattern
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-\w%!.~\'()*+,;=:@&=]*)*(?:\?[-\w%.!~\'()*+,;=:@&=/?]*)?(?:#[-\w%.!~\'()*+,;=:@&=/?]*)?'
    
    # Find all URLs in the text
    urls = re.findall(url_pattern, text)
    
    # Return unique URLs
    return list(dict.fromkeys(urls))

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get API key from session or environment
    api_key = session.get('api_key') or os.environ.get("PERPLEXITY_API_KEY")
    search_history = get_search_history()
    selected_items = get_selected_items()
    
    if request.method == 'POST':
        # Handle settings submission
        if 'save_settings' in request.form or 'save_api_key' in request.form:
            # Process API key
            new_api_key = request.form.get('api_key', '').strip()
            if new_api_key:
                session['api_key'] = new_api_key
                flash('API key saved successfully', 'success')
            elif 'api_key' in request.form and not new_api_key:
                session.pop('api_key', None)
                flash('API key removed', 'info')
            
            # Process website URL (only if save_settings was used)
            if 'save_settings' in request.form and 'website_url' in request.form:
                website_url = request.form.get('website_url', '').strip()
                # No need to store in session as it's handled by localStorage in the browser
                if website_url:
                    flash('Website URL saved successfully', 'success')
            
            return redirect(url_for('index'))
            
        # Handle search form submission
        elif 'query' in request.form:
            query = request.form['query']
            model = request.form.get('model', 'sonar-deep-research')
            
            if not query:
                flash('Please enter a search query', 'error')
                return redirect(url_for('index'))
            
            if not api_key:
                flash('API key not found. Please set your API key in the settings.', 'error')
                return redirect(url_for('index'))
            
            # Call Perplexity API
            response = query_perplexity(query, api_key, model)
            
            # Process response
            if "choices" in response:
                response_text = response["choices"][0]["message"]["content"]
                
                # Extract URLs from the response
                extracted_urls = extract_urls(response_text)
                
                result = {
                    'query': query,
                    'model': model,
                    'response': response_text,
                    'timestamp': response.get("created", ""),
                    'urls': extracted_urls
                }
                
                # Add to search history
                search_history.insert(0, result)
                session['search_history'] = search_history[:10]  # Keep only the 10 most recent searches
                
                if extracted_urls:
                    flash(f'Search completed successfully. Found {len(extracted_urls)} URLs.', 'success')
                else:
                    flash('Search completed successfully. No URLs found.', 'info')
            else:
                flash(f'Error: {json.dumps(response)}', 'error')
        
        # Handle selection for next stage
        elif 'select_item' in request.form:
            item_index = int(request.form['select_item'])
            if 0 <= item_index < len(search_history):
                selected_item = search_history[item_index]
                if selected_item not in selected_items:
                    selected_items.append(selected_item)
                    session['selected_items'] = selected_items
                    flash('Item added to selection', 'success')
                else:
                    flash('Item already selected', 'info')
        
        # Handle URL selection
        elif 'select_urls' in request.form:
            print("DEBUG: select_urls form submitted")
            print(f"DEBUG: Form data: {request.form}")
            
            try:
                item_index = int(request.form['item_index'])
                print(f"DEBUG: item_index = {item_index}")
                
                if 0 <= item_index < len(search_history):
                    # Get the selected URLs from the form
                    selected_urls = request.form.getlist('url_checkbox')
                    print(f"DEBUG: selected_urls = {selected_urls}")
                    
                    # Get the current selected URLs
                    all_selected_urls = get_selected_urls()
                    print(f"DEBUG: all_selected_urls before = {all_selected_urls}")
                    
                    # Add newly selected URLs
                    added_count = 0
                    for url in selected_urls:
                        if url not in all_selected_urls:
                            all_selected_urls.append(url)
                            added_count += 1
                    
                    # Update session
                    session['selected_urls'] = all_selected_urls
                    print(f"DEBUG: all_selected_urls after = {all_selected_urls}")
                    
                    if added_count > 0:
                        flash(f'Added {added_count} URLs to selection', 'success')
                    else:
                        flash('No new URLs were added to selection', 'info')
                else:
                    print(f"DEBUG: item_index {item_index} out of range (0-{len(search_history)-1})")
                    flash('Invalid item index', 'error')
            except Exception as e:
                print(f"DEBUG: Exception in select_urls: {str(e)}")
                flash(f'Error processing URL selection: {str(e)}', 'error')
        
        # Handle removal from selection
        elif 'remove_item' in request.form:
            item_index = int(request.form['remove_item'])
            if 0 <= item_index < len(selected_items):
                selected_items.pop(item_index)
                session['selected_items'] = selected_items
                flash('Item removed from selection', 'success')
        
        # Handle clearing history
        elif 'clear_history' in request.form:
            session['search_history'] = []
            flash('Search history cleared', 'success')
        
        # Handle clearing selection
        elif 'clear_selection' in request.form:
            session['selected_items'] = []
            flash('Selection cleared', 'success')
        
        return redirect(url_for('index'))
    
    # GET request - render the template
    return render_template('index.html', 
                          search_history=search_history, 
                          selected_items=selected_items,
                          selected_urls=get_selected_urls(),
                          api_key_set=bool(api_key))

@app.route('/next_stage', methods=['POST'])
def next_stage():
    selected_items = get_selected_items()
    selected_urls = get_selected_urls()
    
    if not selected_items and not selected_urls:
        flash('No items or URLs selected for the next stage', 'error')
        return redirect(url_for('index'))
    
    # Here you would implement the logic for the next stage
    # For now, we'll just display the selected items and URLs
    return render_template('next_stage.html', 
                          selected_items=selected_items,
                          selected_urls=selected_urls)

@app.route('/clear_selected_urls', methods=['POST'])
def clear_selected_urls():
    session['selected_urls'] = []
    flash('Selected URLs cleared', 'success')
    return redirect(url_for('index'))

@app.route('/remove_url', methods=['POST'])
def remove_url():
    url = request.form.get('url')
    if url:
        selected_urls = get_selected_urls()
        if url in selected_urls:
            selected_urls.remove(url)
            session['selected_urls'] = selected_urls
            flash('URL removed from selection', 'success')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
