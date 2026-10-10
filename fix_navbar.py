import glob
import re

files = [
    'index.html',
    'home2.html',
    'programs.html',
    'instructors.html',
    'water safety.html',
    'schedules.html',
    'contact.html',
    'navbar.html'
]

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update media query max-width from 1180px to 1280px
    content = content.replace('@media (max-width: 1180px)', '@media (max-width: 1280px)')

    # 2. Update .navbar-container styles if present
    content = re.sub(
        r'\.navbar-container\s*\{[^}]*\}',
        '''.navbar-container {
            max-width: 1440px;
            margin: 0 auto;
            padding: 0.75rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            white-space: nowrap;
        }''',
        content,
        count=1
    )

    # 3. Add flex-shrink: 0 to nav-logo, nav-center-menu, nav-right-actions if needed
    if '.nav-logo {' in content:
        content = re.sub(
            r'(\.nav-logo\s*\{[^}]*?)\}',
            r'\1 flex-shrink: 0; }',
            content,
            count=1
        )
        # remove duplicate flex-shrink if added twice
        content = content.replace('flex-shrink: 0; flex-shrink: 0;', 'flex-shrink: 0;')

    if '.nav-center-menu {' in content:
        content = re.sub(
            r'(\.nav-center-menu\s*\{[^}]*?)\}',
            r'\1 flex-shrink: 0; }',
            content,
            count=1
        )
        content = content.replace('flex-shrink: 0; flex-shrink: 0;', 'flex-shrink: 0;')

    if '.nav-right-actions {' in content:
        content = re.sub(
            r'(\.nav-right-actions\s*\{[^}]*?)\}',
            r'\1 flex-shrink: 0; }',
            content,
            count=1
        )
        content = content.replace('flex-shrink: 0; flex-shrink: 0;', 'flex-shrink: 0;')

    # 4. Update .nav-link padding
    content = re.sub(
        r'(\.nav-link\s*\{[^}]*?padding:\s*)0\.55rem 0\.95rem;',
        r'\1 0.5rem 0.75rem;',
        content
    )

    # 5. Update .action-chip padding
    content = re.sub(
        r'(\.action-chip\s*\{[^}]*?padding:\s*)0\.45rem 0\.95rem;',
        r'\1 0.4rem 0.85rem;',
        content
    )

    # Determine which nav-link is active
    active_page = None
    if filename == 'index.html': active_page = 'home'
    elif filename == 'home2.html': active_page = 'home2'
    elif filename == 'programs.html': active_page = 'programs'
    elif filename == 'instructors.html': active_page = 'instructors'
    elif filename == 'schedules.html': active_page = 'schedules'
    elif filename == 'water safety.html': active_page = 'watersafety'
    elif filename == 'contact.html': active_page = 'contact'
    elif filename == 'navbar.html': active_page = 'home'

    # Build Header Nav HTML with correct order:
    # Home -> Programs -> Instructors -> Schedules -> Water Safety -> Contact -> Dashboard
    home_active = ' active' if active_page in ['home', 'home2'] else ''
    prog_active = ' active' if active_page == 'programs' else ''
    inst_active = ' active' if active_page == 'instructors' else ''
    sched_active = ' active' if active_page == 'schedules' else ''
    ws_active = ' active' if active_page == 'watersafety' else ''
    cnt_active = ' active' if active_page == 'contact' else ''

    new_header_menu = f'''<ul class="nav-center-menu">
                <li class="nav-item dropdown">
                    <a href="index.html" class="nav-link{home_active}">
                        Home <i class="fas fa-chevron-down dropdown-caret"></i>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a href="index.html" class="dropdown-item"><span>Home 1 (Water Confidence)</span></a></li>
                        <li><a href="home2.html" class="dropdown-item"><span>Home 2 (Stroke Mastery)</span></a></li>
                    </ul>
                </li>
                <li class="nav-item"><a href="programs.html" class="nav-link{prog_active}">Programs</a></li>
                <li class="nav-item"><a href="instructors.html" class="nav-link{inst_active}">Instructors</a></li>
                <li class="nav-item"><a href="schedules.html" class="nav-link{sched_active}">Schedules</a></li>
                <li class="nav-item"><a href="water safety.html" class="nav-link{ws_active}">Water Safety</a></li>
                <li class="nav-item"><a href="contact.html" class="nav-link{cnt_active}">Contact</a></li>
                <li class="nav-item dropdown">
                    <a href="#" class="nav-link">
                        Dashboard <i class="fas fa-chevron-down dropdown-caret"></i>
                    </a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="user-dashboard.html" class="dropdown-item parent-dash">
                                <div>
                                    <div style="font-weight: 700;">User Dashboard</div>
                                    <div style="font-size: 0.78rem; color: var(--text-muted);">Learning Topics, Badges &amp; Levels</div>
                                </div>
                                <span class="dash-pill parent">Family</span>
                            </a>
                        </li>
                        <li>
                            <a href="admin-dashboard.html" class="dropdown-item admin-dash">
                                <div>
                                    <div style="font-weight: 700;">Admin Dashboard</div>
                                    <div style="font-size: 0.78rem; color: var(--text-muted);">Rosters, Coaches &amp; Billing</div>
                                </div>
                                <span class="dash-pill admin">Staff</span>
                            </a>
                        </li>
                    </ul>
                </li>
            </ul>'''

    # Replace <ul class="nav-center-menu">...</ul>
    content = re.sub(
        r'<ul class="nav-center-menu">[\s\S]*?</ul>\s*(?=<div class="nav-right-actions")',
        new_header_menu + '\n\n            ',
        content
    )

    # Build Mobile Drawer HTML in matching order
    new_mobile_items = f'''<li class="mobile-item" style="border: none; padding: 0.5rem 0.5rem 0.2rem 0.5rem; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.6px;">Main Navigation</li>
            
            <li class="mobile-item">
                <div class="mobile-link" id="mobileHomeAcc">
                    <span><i class="fas fa-home" style="width: 24px; color: var(--brand-primary);"></i> Home Pages</span>
                    <i class="fas fa-chevron-down dropdown-caret"></i>
                </div>
                <ul class="mobile-accordion" id="mobileHomeContent">
                    <li><a href="index.html" class="mobile-sublink"><i class="fas fa-water" style="width: 18px;"></i> Home 1 (Confidence)</a></li>
                    <li><a href="home2.html" class="mobile-sublink"><i class="fas fa-award" style="width: 18px;"></i> Home 2 (Mastery)</a></li>
                </ul>
            </li>
            
            <li class="mobile-item">
                <a href="programs.html" class="mobile-link">
                    <span><i class="fas fa-swimmer" style="width: 24px; color: var(--brand-aqua);"></i> Swim Programs</span>
                </a>
            </li>
            <li class="mobile-item">
                <a href="instructors.html" class="mobile-link">
                    <span><i class="fas fa-user-nurse" style="width: 24px; color: #f59e0b;"></i> Instructors &amp; Staff</span>
                </a>
            </li>
            <li class="mobile-item">
                <a href="schedules.html" class="mobile-link">
                    <span><i class="fas fa-calendar-alt" style="width: 24px; color: var(--brand-aqua);"></i> Schedules &amp; Slots</span>
                </a>
            </li>
            <li class="mobile-item">
                <a href="water safety.html" class="mobile-link">
                    <span><i class="fas fa-life-ring" style="width: 24px; color: var(--brand-coral);"></i> Water Safety</span>
                </a>
            </li>
            <li class="mobile-item">
                <a href="contact.html" class="mobile-link">
                    <span><i class="fas fa-envelope" style="width: 24px; color: var(--brand-mint);"></i> Contact Us</span>
                </a>
            </li>'''

    content = re.sub(
        r'<li class="mobile-item" style="border: none; padding: 0\.5rem 0\.5rem 0\.2rem 0\.5rem;[\s\S]*?(?=<li class="mobile-item" style="border: none; padding: 0\.75rem 0\.5rem 0\.2rem 0\.5rem; font-size: 0\.72rem; font-weight: 800; text-transform: uppercase; color: var\(--text-muted\); letter-spacing: 0\.6px;">Dashboards &amp; Portals)',
        new_mobile_items + '\n\n            ',
        content
    )

    # Build Footer Quick Links in matching order
    new_footer_quick_links = '''<h4>Quick Links</h4>
                <ul class="footer-links">
                    <li><a href="programs.html" class="footer-link"><i class="fas fa-chevron-right"></i> Programs</a></li>
                    <li><a href="instructors.html" class="footer-link"><i class="fas fa-chevron-right"></i> Instructors</a></li>
                    <li><a href="schedules.html" class="footer-link"><i class="fas fa-chevron-right"></i> Schedules</a></li>
                    <li><a href="water safety.html" class="footer-link"><i class="fas fa-chevron-right"></i> Water Safety</a></li>
                    <li><a href="contact.html" class="footer-link"><i class="fas fa-chevron-right"></i> Contact Us</a></li>
                </ul>'''

    content = re.sub(
        r'<h4>Quick Links</h4>\s*<ul class="footer-links">[\s\S]*?</ul>',
        new_footer_quick_links,
        content
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {filename}")

for f in files:
    update_file(f)
