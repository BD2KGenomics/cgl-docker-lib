/opt/tachyon/bin/tachyon format
/opt/tachyon/bin/tachyon bootstrap-conf $1
/opt/tachyon/bin/tachyon-start.sh worker SudoMount

tail -f /opt/tachyon/logs/*
