Summary:	A tabbed SSH connection manager for GTK+ environments
Name:		gnome-connection-manager
Version:	1.1.0
Release:	1%{?dist}

License:	GPLv3 and MIT
URL:		http://kuthulu.com/gcm/

Source0:	http://kuthulu.com/gcm/%{name}_%{version}_all.tgz
Source1:	LICENSES
Source2:	%{name}.desktop
Source3:	%{name}.sh
Source4:	%{name}.appdata.xml
Patch0:		gcm-1.1.0-fix-l2k1.patch

BuildArch:	noarch

BuildRequires:	vte
BuildRequires:	python
BuildRequires:	desktop-file-utils

Requires:	vte
Requires:	expect
Requires:	pygtk2-libglade

%description
Gnome Connection Manager is a tabbed SSH connection manager for GTK+
environments.

%prep
%setup -q -n gcm-%{version}
%patch0 -p1
# update Russian translation
msgfmt -o  lang/ru/LC_MESSAGES/gcm-lang.mo lang/ru_RU.po

# Remove pre-compiled files
find . -name "*.pyc" -exec rm -f {} \;
find . -name "*.pyo" -exec rm -f {} \;

# Upstream does not include a copy of the licences
cp -p %{SOURCE1} .

# Fix shebang line
sed -i -e 's/^#!.*//' pyAES.py

%build
#Nothing to build

%install
# Install application
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr *.py *.glade ssh.expect *.gif *.png %{buildroot}%{_datadir}/%{name}

# Install icon and desktop file
install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -p -m 644 icon.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category GNOME \
  --add-category GTK \
  --add-category Utility \
  %{SOURCE2}

# Install start script
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE3} %{buildroot}%{_bindir}/%{name}

# Install appdata
install -d -m 755 %{buildroot}%{_datadir}/appdata
install -p -m 644 %{SOURCE4} %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

# Install locales
install -d -m 755 %{buildroot}%{_datadir}/locale
cp -r  lang/ %{buildroot}%{_datadir}/%{name} 
cp -pr lang/?? %{buildroot}%{_datadir}/locale
%find_lang gcm-lang

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files -f gcm-lang.lang
%doc LICENSES
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Mon Nov 16 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 1.1.0-1.R
- initial build with merger Mat Booth spec
- fix Russian translation
